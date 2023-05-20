# oasis README

A small plugin that is built on top text-generation-web-ui API.

## Features

This extension adds four commands that are applicable to your current selected code in the editor:

1. Add docstrings to selection
2. Add unit tests to the selection
3. Fix syntax errors on the selection.
4. Improve code quality on the selection.

All of these commands are highly experimental and there's no warranty to produce good results.
Use at your own risk :)

## Requirements

You need to setup text-generation-web-ui: https://github.com/oobabooga/text-generation-webui

## Extension Settings

There are no pre-defined settings for this extension. It should add the following commands to your environment:

```
onCommand:oasis.addDocstring
onCommand:oasis.addTypeHints
onCommand:oasis.fixSyntaxError
onCommand:oasis.improveCodeQuality
```

You can bind these to your favorite key.

I'd look into making it more flexible in the future.

## Known Issues

## Release Notes

### 0.1.0

1. Add docstrings to selection.
2. Add unit tests to the selection.
3. Fix syntax errors on the selection.
4. Improve code quality on the selection.