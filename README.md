<p align="center">
  <a href="https://opencode.ai">
    <picture>
      <img src="assets/opencode-vibe.png" alt="OpenCode vibe logo" style="height: 180px">
    </picture>
  </a>
</p>

# opencode-vibe: opencode agent as a Docker container

<a href="https://www.npmjs.com/package/opencode-ai"><img alt="npm" src="https://img.shields.io/npm/v/opencode-ai?style=flat-square" /></a>
[![build opencode Docker image](https://github.com/didier-durand/opencode-vibe/actions/workflows/build-docker-opencode.yaml/badge.svg)](https://github.com/didier-durand/opencode-vibe/actions/workflows/build-docker-opencode.yaml)


The GitHub workflow and Dockerfile of this repo create a full-stack container image based on Debian (currently Trixie) 
to run [Opencode](https://opencode.ai/), aka *"the Open Source coding agent"*.  Running opencode in Docker keeps it 
fully fledged: you can still run the agent in advanced terminals like [Ghostty](https://ghostty.org/docs/about) 
or [Alacritty](https://github.com/alacritty/alacritty) to enjoy the optimal User Experience (UX).

Give it try: in your Ghostty / Alacritty / regular terminal, just execute 

`docker run -it ghcr.io/didier-durand/opencode-vibe:latest opencode --log-level INFO --model opencode/glm-4.7-free --prompt 'who are you?'`

Opencode will answer you who he is. The model `opencode/glm-4.7-free` is a free model, based on z.AI GLM-4.7, offered by Opencode to make initial steps.

OpenTelemetry collector is embarked to make your various Opencode instances fully and efficiently 
observable wherever you run them (laptop, open-prem server, cloud). Good [observability](https://www.ibm.com/think/topics/observability)
is critical to the success of agentic AI project: this [IBM article](https://www.ibm.com/think/insights/ai-agent-observability)
explains in all details the importance of full observability in agentic workflows. Our [Substack article](https://didierdurand.substack.com/p/opentelemetry-the-glass-box-in-the) 
explains why we believe that OpenTelemetry is the right framework to observe our agents.

## Why in a container ?

We only run Opencode and similar agents like Claude Code, Gemini CLI, etc. in containers. Why? 

* To be able to give Opencode full autonomy in tool use and data access within the container or on carefully 
chosen / isolated disk sections (mounted as Docker runtime volumes). It gives the agents the 
opportunity to deliver their maximum value as they have no constraints. The isolation provided by 
the container makes it riskless for the setup and content of the host machine (local laptop, cloud server, etc.)
* To obtain repeatability and consistency: we run same agents in diverse environments (laptop, on-premise infrastructure, cloud 
server, etc.) for diverse parts of our workflows. Executing agents in a container ensures that their 
technical environments (dependencies, etc.) are always identical. The number of setup-related issues
gets massively reduced and the agent behaviors are consistent across those distinct environment.
* To achieve portability: as a corollary of previous bullet, same container image can easily run 
anywhere. So, we can develop and optimize an agentic workflow on a laptop and move to the cloud 
for productive use.

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
4. Install OpenTelemetry with all its community contributions: Opencode leverages OpenTelemetry
(via [Vercel's AI SDK](https://ai-sdk.dev/)) to report logs, trace spans, etc. The configuration in 
[otel-config.yaml](otel-config.yaml) has provisions via environment variables to specify OpenTelemetry 
endpoint at runtime in the `docker run` command.
5.  Install last version of opencode via npm. It runs under a specific user `opencode` 
in its home directory to avoid the use of root.
6. Push the built image in GitHub-provided container repository `ghcr.io/didier-durand/opencode-vibe:latest`
7. Download the new version of the Docker image just pushed
8. Execute Opencode with a basic prompt to ensure and check the response to make sure that the 
image is functioning as expected.

Feel free to download and use this image as needed or customize the Dockerfile for your use case.

For a quick start, use our version. Just pull it: `docker pull ghcr.io/didier-durand/opencode-vibe:latest`
