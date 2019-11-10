# tint

A theme switcher.

Idea:
 
- have a yaml theme file
- hava a declarative file that specifies where a theme should be
  applied.
- have another file that is a script that is run after the configs
  were updated.

In the yaml file specify a tree of properties (colors etc, like
i3-style) In the configs always specify colors like this
{{basecolor.yellow}} or something like that.

there should always be a file like that
.config/i3/config.template
and from that the tool will make
.config/i3.config

then in the script I run
i3-reload

and that's it.


jinja templating

yaml file for config


by default the themes can live in

~/.config/tint/themes/

in the yaml I can specify paths to hook scripts that should be run.

I should be able to specify a base yaml, where I can configure script
paths and files to update etc.  In yaml it is also possible to specify
lists.

~/.config/tint/scripts/



## Inspiration

j4-make-config
i3-style
