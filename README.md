# Hover Locales

A Sublime Text 3 plugin to show different locales strings simply by hovering on a localized string.

![Screenshot of Hover Locales, a plugin for Sublime Text 3 by @alvesjtiago](http://i.imgur.com/FJhzzYP.png)

## Installation

### Package Control

Hover Locales has been approved on Package Control! 🎉
Search for "Hover Locales" and install.

### Manual

_macOS_
```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
git clone --depth=1 https://github.com/alvesjtiago/hover-locales.git
```

_Ubuntu_
```
cd ~/.config/sublime-text-3/Packages
git clone --depth=1 https://github.com/alvesjtiago/hover-locales.git
```

_Windows_
```
cd "%APPDATA%\Sublime Text 3\Packages"
git clone --depth=1 https://github.com/alvesjtiago/hover-locales.git
```

Or manually create a folder named "hover-locales" on your Packages folder and copy the content of this repo to it.

## Configuration

#### scopes
Scopes that trigger locales search, (default: `["text.find-in-files", "text.html.ruby", "source.ruby"]`).

#### locales_path
Path to search for .yml locales files, (default: `"config/locales"`).

## Contribute

Hover Locales is a small utility created by [Tiago Alves](https://twitter.com/alvesjtiago).
Any help on this project is more than welcome. Or if you find any problems, please comment or open an issue with as much information as you can provide.
