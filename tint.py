#!/usr/bin/env python3
import argparse
import os
import os.path
import subprocess
import yaml
from tempfile import NamedTemporaryFile
from jinja2 import Template


THEMES_DIR = os.path.expanduser('~/.config/tint/themes/')
SCRIPTS_DIR = os.path.expanduser('~/.config/tint/scripts/')


def merge_two_dicts(config, base, path=None):
    """Merges two configs, overwriting properties in the base."""
    assert config is not None
    assert base is not None
    final = {}
    keys = set()
    keys.update(config.keys())
    keys.update(base.keys())
    for key in keys:
        # key only in config
        if (key in config) and (key not in base):
            final[key] = config[key]
        # key only in base
        elif key not in config and key in base:
            final[key] = base[key]
        # key is in both of them
        else:
            assert key in config
            assert key in base
            # both key values are dicts, recurse
            if isinstance(config[key], dict) and isinstance(base[key], dict):
                final[key] = merge_two_dicts(config[key],
                                             base[key],
                                             path=f"{path}.{key}")
            # neither of them are dicts: config has preference
            elif not isinstance(config[key], dict) and not isinstance(base[key], dict):
                final[key] = config[key]
            # something doesn't add up ...
            else:
                raise ValueError(f"Types don't match: {path}: {key}")
    return final


def merge_configs(configs):
    """Takes a list of configs and merges them, with the first one taking
    precedence over the subsequent ones."""
    config = {}
    print(f"received {len(configs)} configs")
    print(configs)
    for base in configs:
        print("asdfasdfasdfasdfasdf")
        print(config)
        print(base)
        config = merge_two_dicts(config, base)
    return config


def traverse(config_or_value, out, path):
    c = config_or_value
    if isinstance(c, dict):
#        return {key: traverse(c[key], 
#        for key in config_or_value:
        pass


def get_path_in_dict(d, path):
    val = d
    while len(path) > 0 and val is not None:
        val = val.get(path[0], None)
        path = path[1:]
    return val


def set_path_in_dict(d, path, val):
    current = d
    while len(path) > 1:
        if path[0] not in current:
            current[path[0]] = {}
        current = current[path[0]]
        path = path[1:]
    current[path[0]] = val


def resolve_config(config):
    new_config = {}
    stack = [((), config)]
    while len(stack) > 0:
        path, cv = stack.pop()  # cv: config or value
        if isinstance(cv, dict):
            for key, val in cv.items():
                stack.append((path + (key,), val))
        elif isinstance(cv, str) and cv.startswith('->'):
            target_path = tuple(cv[2:].split('.'))
            val = get_path_in_dict(config, target_path)
            set_path_in_dict(new_config, path, val)  # set directly, no further resolving.
        else:
            set_path_in_dict(new_config, path, cv)
    return new_config


def load_config(config_path: str):
    """Loads a config file from a path.
    Reads the base config and merges it.
    Resolves reference keys."""
    configs = []
    while config_path is not None:
        print(f'loading {config_path}')
        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
            configs.append(config)
            print(config)
            base_filename = config.get('meta', {}).get('base', None)
            if base_filename is not None:
                config_path = os.path.join(THEMES_DIR, base_filename)
            else:
                config_path = None
    config = merge_configs(configs)
    config = resolve_config(config)
    return config


def process_template(template_path, out_path, props):
    with open(template_path, 'r') as f:
        template = Template(f.read())
    out = template.render(props)
    with open(out_path, 'w') as f:
        f.write(out)


def process_hooks(hook_files, props):
    for hook_file in hook_files:
        with open(hook_file, 'r') as f:
            template = Template(f.read())
        out = template.render(props)
        with NamedTemporaryFile(mode='w') as f:
            print(f.name)
            f.write(out)
            f.flush()
            subprocess.run(['sh', f.name])


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    set_theme = subparsers.add_parser('set', help='Set current theme.')
    set_theme.add_argument('theme',
                           help='The theme to set. (use list to show themes).')

    edit_theme = subparsers.add_parser('edit', help='Editing themes.')
    edit_theme.add_argument('theme',
                            help='Opens the theme config with $EDITOR.')

    list_themes = subparsers.add_parser('ls', help='Display themes.')

    args = parser.parse_args()
    return args


def set_theme(theme):
    config_path = os.path.join(THEMES_DIR, theme + '.yaml')
    config = load_config(config_path)
    config['home'] = os.path.expanduser('~')
    # generate paths
    paths = [os.path.expanduser(p) for p in config['meta']['paths'].values()]
    for path in paths:
        process_template(path + '.template', path, config)
    # run hooks
    hooks = [os.path.join(SCRIPTS_DIR, script_file)
             for script_file in config['meta']['hooks']['post_generate']]
    process_hooks(hooks, config)


def edit_theme(theme):
    print('Not implemented yet.')


def list_themes():
    themes = [filename
              for filename in os.listdir(THEMES_DIR)
              if filename.endswith('.yaml')]
    for filename in themes:
        theme_name = filename[:-5]
        theme_path = os.path.join(THEMES_DIR, filename)
        config = load_config(theme_path)
        desc = config.get('meta', None).get('description', None)
        print(f"{theme_name} - {desc}")


def main():
    # read args and theme config
    args = parse_args()
    if args.cmd == 'set':
        set_theme(args.theme)
    elif args.cmd == 'edit':
        edit_theme(args.theme)
    elif args.cmd == 'ls':
        list_themes()
    else:
        print("Command not implemented yet!")


if __name__ == '__main__':
    main()
