# Hornero

> A package selector for building your comfy nest

## About

Hornero helps you to install your favourite packages on your fresh installed
Linux distribution. It expects you to pass a simple
[YAML](https://en.wikipedia.org/wiki/YAML) file containing a list of your
favourite packages, which are automatically installed by it. Therefore you only
need to keep an updated list of your favourite packages in order to quickly
install them the next time you reinstall your distro. It can also be helpful
for sysadmins that need to perform Linux installations on several machines by
saving time on the post install process.

> ### The name
>
> The [hornero](https://en.wikipedia.org/wiki/Hornero) is a type of bird native
> from South America well known for building mud nests that look like
> wood-fired ovens, therefore its name: _hornero_ derivates from the Spanish
> word _horno_ that means oven.


## How to install

You need `pip` (or `pip3`, depending on which distro are you running) to
install `hornero`.
Then run:

```bash
pip install git+git://github.com/santisoler/hornero.git
```

or

```bash
pip3 install git+git://github.com/santisoler/hornero.git
```

## How to use

We need to write a `packages.yml` file containing the packages we will
eventually want to install in the future.
All packages must be grouped inside categories.
For example:

```yaml
basic:
  - git
  - gnupg
  - neovim

graphics:
  - gimp
  - inkscape
  - krita

system:
  - gnome-disk-utility
  - gnome-system-monitor
```

We can then run `hornero` from the command line passing the `packages.yml` file
as argument:

```bash
hornero packages.yml
```

`hornero` will ask us to choose one or more categories, so only the packages
inside the chosen categories will be installed.
Therefore we can include any package we eventually use on `packages.yml`, but
choose which packages we definitely want to install after a fresh Linux
installation.

## License

All content under [MIT License](https://mit-license.org/), except where noted.
