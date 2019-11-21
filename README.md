# tint

A theme switcher.

`tint` allows fast and convenient theme switching for all your
applications such as `i3`, `rofi` and `urxvt`.

It works by by processing config *templates* in which the actual color
codes are filled in.

A theme is defined in a `yaml` file (see `leuven.yaml` for an
example).  In there properties and colors are defined.  A config
template could then look like this:

```
rofi.color-normal: {{rofi.bg}}, {{rofi.fg}}, {{rofi.bgalt}}, {{rofi.hlbg}}, {{rofi.hlfg}}
rofi.color-window: {{rofi.background}}, {{rofi.border}}

rofi.width: 20

rofi.font: inconsolata 14
```

The `{{...}}` syntax is part of the templating engine.  It is replaced
by a property defined in the theme.

The template defines which config files to process in a `paths`
section:

```
paths:
  - ~/.config/i3/config
  - ~/.config/rofi/config
  - ~/.Xdefaults
```

for every `<path>` it expects the file `<path>.template` to be
present.  If present, it will generate the config file from the
template.

## Base themes

config files can specify a base theme in `meta.base`.  The base theme
must be another theme in the themes directory.  Before the config is
applied, the base theme is loaded.  Properties defined in the theme
itself take precedence over properties defined in the base.


## Dependencies

Dependencies are in the `requirements.txt`

- *PyYAML*: For reading the yaml files
- *jinja2*: For handling the templating


## Some more things

Uses jinja for templating.

This project was inspired by
(i3-style)[https://github.com/altdesktop/i3-style], from which the
idea of using a `yaml` configuration file was taken.

The idea to use templating was also inspired by
(j4-make-config)[https://github.com/okraits/j4-make-config].

Add variable expansion in the paths.

Works well with `urxvt` and
(urxvt-config-reload)[https://github.com/regnarg/urxvt-config-reload],
which allows to trigger reloading of urxvt config in urxvt instances.
For example:

```
xrdb -merge ~/.Xdefaults

pids=$(ps axo pid,comm | grep "^[ 0-9]* urxvt\$" | awk "{print \$1}")

for pid in $pids
do
    kill -1 $pid  # send SIGHUP
    echo "TEST $pid"
done
```
