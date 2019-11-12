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


def load_config(path: str):
    """Loads a config file from a path)"""
    with open(path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
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
    paths = [os.path.expanduser(p) for p in config['paths'].values()]
    for path in paths:
        process_template(path + '.template', path, config)
    # run hooks
    hooks = [os.path.join(SCRIPTS_DIR, script_file)
             for script_file in config['hooks']['post_generate']]
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
    if args.cmd == 'edit':
        edit_theme(args.theme)
    if args.cmd == 'ls':
        list_themes()
    else:
        print("Command not implemented yet!")


if __name__ == '__main__':
    main()
