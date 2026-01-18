
# opencode-vibe

[![GitHub version](https://badge.fury.io/gh/anomalyco%2Fopencode.svg)](https://badge.fury.io/gh/anomalyco%2Fopencode)[![build opencode Docker image](https://github.com/didier-durand/opencode-vibe/actions/workflows/build-docker-opencode.yaml/badge.svg)](https://github.com/didier-durand/opencode-vibe/actions/workflows/build-docker-opencode.yaml)


The Dockerfile of this repo creates of full-stack container image based on Debian (currently Trixie) 
to run [Opencode](https://opencode.ai/), aka *"the Open Source coding agent"*.  Running opencode in Docker doesn't 
reduce its functionality: you can still run opencode within [Ghostty](https://ghostty.org/docs/about) 
or [Alacritty](https://github.com/alacritty/alacritty) to enjoy the 
optimal User Experience (UX).

## Why in a container ?

We only run Opencode (and similar agents like Claude Code, Gemini CLI, etc.) in a container. Why? 

* To be able to give Opencode full autonomy in tool use and data access within the container or on carefully 
chosen / isolated disk sections (mounted as Docker runtime volumes). That is the best way to give them the 
opportunity to deliver their maximum value. The isolation provided by the container makes it 
riskless for the setup and content of the host machine (local laptop, cloud server, etc.)
* To obtain repeatability: we run agents in diverse setups (laptop, on-premise infrastructure, cloud 
server, etc.) for diverse parts of our workflows. Executing agents in a container ensures that their 
technical environment (dependencies, etc.) are always identical. The number of setup-related issues
gets massively reduced.

## Image build workflow

Our [GitHub workflow](.github/workflows/build-docker-opencode.yaml) automatically builds a new version of the Docker image for x86 and arm64 
architectures every 12h as Opencode currently evolves very fast. It is stored in thr [public container repository](https://github.com/didier-durand/opencode-vibe/pkgs/container/opencode-vibe)
of this repository. The version badge displays the last [known version of Opencode package](https://github.com/anomalyco/opencode/releases) 
configured in the image.

To raise image quality, the GitHub action checks the snytax of the [Dockerfile](Dockerfile) via [Hadolint](https://github.com/hadolint/hadolint). 
The utility check-jsonchema is used to validate the configuration [opencode.jsonc](https://opencode.ai/docs/config/) 
against the opencode JSON schema pushlished at [https://opencode.ai/config.json](https://opencode.ai/config.json)

the [Dockerfile](Dockerfile) is based on Debian v13, aka Trixie, official image. 

The build workflow will:
1. refresh Trixie's package
2. install a set of foundational system tools like wget, url, jq, etc. very often within the bash 
tools of opencode. This upfront installation avoids opencode to install them needed: it save LLM 
tokens and reduces response latency.
3. Install Python and uv: coding agents like opencode tend often to generate small scripts when they 
need to repeat same operation against multiple application files. The pre-installation avoid 
opencode having to install it on first use.
4. Install OpenTelemetry with all its community contributions: good [observability](https://www.ibm.com/think/topics/observability)
is [critical to the success](https://www.ibm.com/think/topics/observability) of agentic AI project. 
Opencode leverages OpenTelemetry (via [Vercel's AI SDK](https://ai-sdk.dev/)) to report logs, trace 
spans, etc. We explained on our Substack the key aspects of OpenTelemetry that make it so valuable 
in agentic contexts.
5.  Install last version of opencode via npm. It runs under a specific user `opencode` 
in its home directory to avoid the use of root.
6. Push the built image in GitHub-provided container repository `ghcr.io/didier-durand/opencode-vibe:latest`
7. Download the new version of the Docker image just pushed and execute opencode with a minimal prompt 
to ensure that the image is functioning as expected.

Feel free to download and use this image as needed or customize the Dockerfile for your use case.

To use our version, just pull it: `docker pull ghcr.io/didier-durand/opencode-vibe:latest`
