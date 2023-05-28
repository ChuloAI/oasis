# Oasis


NOTE: main is currently unstable, developing the use of guidance prompts.

Please use tag v0.1.3 for the more stable version (though also not as reliable)

This is still in development, highly experimental.

Change of plans: the idea is to roll not depend on text-generation-webui but on our own server with the guidance library,
to explore the library to it's fullest.

## Local LLamas on VSCode
**WARNING**: does not yet work too well!

### Installation

## If using v.0.1.3
1. Install text-generation-web-ui, start it with API: https://github.com/oobabooga/text-generation-webui

`git clone: https://github.com/paolorechia/oasis@v0.1.3`

2. Start the FastAPI server in `prompt_server`:
```
    cd prompt_server
    pip install -r requirements.txt
    ./start_uvicorn.sh
```


## If using main
`git clone: https://github.com/paolorechia/oasis@main`


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
