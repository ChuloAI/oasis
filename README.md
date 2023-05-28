# Oasis
The idea is generate code with the assistance of guidance library, using open source LLM models that run locally.
This library is exposed as a VSCode plugin, and adds code-generation commands on editor selection (invoked through right-click or command palette).

NOTE: main is currently unstable, developing the use of guidance prompts (see guidance library: https://github.com/microsoft/guidance)

Version v0.1.4 will be released soon, which uses guidance with Salesforce Codegen models. This is still in development, highly experimental.

**WARNING**: Only add docstring to functions command is somewhat stable at the moment.

## Local Codegen Models on VSCode
How does it work?

TODO: add proper explanation here 

### Installation

## If using v0.1.3
If you want to use text-generation-webui with simpler prompts, use v0.1.3. This is a deprecated feature, newer versions will no longer support `text-generation-webui`, at least for the time being.


1. Install text-generation-web-ui, start it with API: https://github.com/oobabooga/text-generation-webui

`git clone: https://github.com/paolorechia/oasis@v0.1.3`

2. Start the FastAPI server in `prompt_server`:
```
    cd prompt_server
    pip install -r requirements.txt
    ./start_uvicorn.sh
```


## If using v0.1.4 or main
Main:
`git clone: https://github.com/paolorechia/oasis@main`

Or v0.1.4:

`git clone: https://github.com/paolorechia/oasis@v0.1.4`


1. Start the FastAPI server in `guidance_server`:
```
    cd guidance_server
    pip install -r requirements.txt
    ./start_uvicorn.sh
```
This server is quite heavy on dependencies, and expects that you can run PyTorch with GPU.


2. Start the FastAPI server in `prompt_server`:
```
    cd prompt_server
    pip install -r requirements.txt
    ./start_uvicorn.sh
```
3. Install VSCode plugin called 'oasis-llamas'
4. Use it!



### Add docstrings to block of code
![Docstring demo](docstring_example.gif)
