# Oasis

## Local LLamas on VSCode

### Installation
1. Install text-generation-web-ui, start it with API: https://github.com/oobabooga/text-generation-webui
2. Start the FastAPI server in `prompt_server`:
```
    git clone: https://github.com/paolorechia/oasis
    cd prompt_server
    pip install -r requirements.txt
    ./start_uvicorn.sh
```
3. Install VSCode plugin called 'oasis-llamas'
4. Use it!

This is still in development, highly experimental. For now we depend on the FastAPI server, the idea is to push all the prompts to the extension config. Unfortunately, I'm a bit too low on time at the moment to do this properly, feel free to contribute with a PR if you'd like :)