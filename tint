#!/usr/bin/env python3
import argparse
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
    parser.add_argument('theme')

    args = parser.parse_args()
    return args


def main():
    # read args and theme config
    args = parse_args()
    config_path = os.path.join(THEMES_DIR, args.theme + '.yaml')
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


if __name__ == '__main__':
    main()
