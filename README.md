## opencode-vibe

The Dockerfile of this repo creates of full container image based on Debian (currently Trixie) to run 
[Opencode](https://opencode.ai/), aka *"the Open Source coding agent"*. 

We only run Opencode (and similar agents like Claude Code, Gemini CLI, etc.) in containers. Why? To 
be able to give them full autonomy in tool use, data access within the container or on carefully 
chosen / isolated disk sections (mounted as Docker volumes). That is the best way to give them the 
opportunity to deliver their maximum value. The isolation provided by the container makes it 
riskless for the setup and content of the host machine (local laptop, cloud server, etc.)

Our [Github workflow](.github/workflows/build-docker-opencode.yaml) automatically builds a new 
version of the Docker image for x86 and arm64 architectures every 12h as Opencode currently evolves 
very fast. It is stored in this [public container repository](https://github.com/didier-durand/opencode-vibe/pkgs/container/opencode-vibe)

Feel free to download and use this image as needed or customize the Dockerfile for your use case.

To do so: `docker pull ghcr.io/didier-durand/opencode-vibe:latest`
