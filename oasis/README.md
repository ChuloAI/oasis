# Oasis Readme
This is still in development, highly experimental. Change of plans: the idea is to roll not depend on text-generation-webui our own server with the guidance library.
Unfortunately, I'm a bit too low on time at the moment to do this properly, feel free to contribute with a PR if you'd like :)

## Local LLamas on VSCode

### Installation
1. Install text-generation-web-ui, start it with API: https://github.com/oobabooga/text-generation-webui
2. Start FastAPI web server from repository: https://github.com/paolorechia/oasis
3. Install this VSCode plugin
4. Use it!

### Configuration
## oasis.prompt_server_url

Defines where the prompt server is hosted. Defaults to http://0.0.0.0:9000