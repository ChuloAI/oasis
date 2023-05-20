# pydex README

A small plugin that is built on top of the OpenAI's Codex API private beta to add a few helper commands for Python programs.

## Features

This extension adds four commands that are applicable to your current selected code in the editor:

1. Add docstrings to selection
2. Add unit tests to the selection
3. Fix syntax errors on the selection.
4. Improve code quality on the selection.

All of these commands are highly experimental and there's no warranty to produce good results.
Use at your own risk :)

## Requirements

You need a pydex token to use this extension. You can signup for free at:

https://signup.codex.openimagegenius.com/signup

## Extension Settings

There are no pre-defined settings for this extension. It should add the following commands to your environment:

```
onCommand:pydex.addDocstring
onCommand:pydex.addTypeHints
onCommand:pydex.fixSyntaxError
onCommand:pydex.improveCodeQuality
```

You can bind these to your favorite key.

## Known Issues


## Release Notes


### 0.1.0

First beta release with the initial features:

1. Google OAuth Signup.
2. Rate limit.
3. Add docstrings to selection.
4. Add unit tests to the selection.
5. Fix syntax errors on the selection.
6. Improve code quality on the selection.