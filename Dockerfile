FROM debian:trixie
SHELL ["/bin/bash", "-c"]
# escape=\

ARG PYTHON_VERSION="3.13"

ENV USER="opencode"
ENV HOME="/home/$USER"
WORKDIR "$HOME"

# hadolint ignore=DL3008
RUN apt-get update -y  \
    && apt-get upgrade -y  \
    && apt-get install -y --no-install-recommends ca-certificates procps jq curl wget unzip git gh nodejs npm \
    && apt-get install -y --no-install-recommends python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION} python3-pip \
    && python3 --version \
    && pip3 --version \
    # clean up \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh  \
    && source /$HOME/.local/bin/env
ENV PATH="$PATH:/$HOME/.local/bin"
RUN uv --version

# install opencode
# hadolint ignore=DL3016,DL3059
RUN npm install -g  opencode-ai
ENV PATH="$PATH:/$HOME/.opencode/bin/"

# this user allows to have all user Opencode data & config on mounted volume
# see https://opencode.ai/docs/troubleshooting/  for content of –/.local
RUN groupadd --system $USER  \
    && useradd --system $USER --gid $USER \
    && chown -R "$USER:$USER"  $HOME
USER "$USER"

CMD ["bash", "-c", "whoami && echo '###' && export GH_TOKEN=$GITHUB_OPENCODE_TOKEN && printenv && sleep infinity"]