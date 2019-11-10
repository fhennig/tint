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


## TODO

include shell script hooks to allow running little scripts like
`i3-reload` or `xrdb -merge ...`.

Handle commandline args.  Handle loading of themes from a default
location (`~/.config/tint/themes/`).

Maybe allow inheritance ...

## Some more things

Uses jinja for templating.

This project was inspired by
(i3-style)[https://github.com/altdesktop/i3-style], from which the
idea of using a `yaml` configuration file was taken.

The idea to use templating was also inspired by
(j4-make-config)[https://github.com/okraits/j4-make-config].

Add variable expansion in the paths.

