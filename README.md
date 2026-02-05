<p align="center">
  <a href="https://opencode.ai">
    <picture>
      <img src="assets/opencode-vibe.png" alt="OpenCode vibe logo" style="height: 180px">
    </picture>
  </a>
</p>

# opencode-vibe: Github-hosted Opencode agent as Moltbook member

<a href="https://www.npmjs.com/package/opencode-ai"><img alt="npm" src="https://img.shields.io/npm/v/opencode-ai?style=flat-square" /></a>
[![build opencode Docker image](https://github.com/didier-durand/opencode-vibe/actions/workflows/build-docker-opencode.yaml/badge.svg)](https://github.com/didier-durand/opencode-vibe/actions/workflows/build-docker-opencode.yaml)

This repository offers 2 main features:
* a way to run an OpenCode agent as a member of Moltbook, the social network for AI agents. Some details about 
Moltbook in [this post](https://didierdurand.substack.com/p/moltbook-the-ai-only-social-network).
* the automated and continuous build of Opencode, the open source coding agent as a full-stack Docker image based on 
Linux Debian. Opencode is my personal choice for AI-based agentic coding ("vibe coding") for the reasons detailed
in [this post](https://didierdurand.substack.com/p/opencode-the-oss-coding-agent-80000). For all technical details
on the Docker image continuous build, read [this page](DOCKER-IMAGE.md)

Go directly to section [Agent Instantiation](#agent-instantiation) below to have your own Opencode agent running on GitHub in minutes
and interacting with peers on Moltbook. It will be 100% free: no costs at all as Opencode team [keeps sponsoring]()https://opencode.ai/docs/zen/ 
the `big-pickle` model.

The main advantage of Opencode as Docker image is to allow it to run on your laptop in a safe and controlled manner. 
It can only access what you allow via [Docker bind mounts at run time](https://docs.docker.com/engine/storage/bind-mounts/). In my use cases, it doesn't need even access 
to any data of my laptop: my Opencode agents clone repositories from GitHub in the Docker container storage, work on them within Docker and send pull requests (PRs) back to GitHub where they are 
accepted or not (sometimes by humans and soemtimes by other agents).

In this repository, the GitHub workflow [run-moltbook-agent.yaml](.github/workflows/run-moltbook-agent.yaml) goes 1 step further. It demonstrates how to run the Opencode Docker image directly on GitHub to 
avoid requiring an external machine like my laptop. 

Additionally, this repository also shows how an Opencode can join the Moltbook social network for AI agents. I developed this solution to 
allow my agents to practice what I'll name "PAD" for "Peer Agentic Development" where multiple independent 
agents collaborate on a shared development goal. Moltbook will allow the discovery of such peers, with whom to 
conduct such a PAD in a dedicated submolt (compared to [subreddits](https://www.reddit.com/r/help/comments/37shum/what_is_a_subreddit/), when Moltbook is defined as "Reddit for 
agents".) if this PAD is executed openly. We'll extend this repository in subsequent versions to show how such PADs can 
happen: it's currently WIP. I believe that various forms of PAA (Peer Agentic Activities) will emerge beyond PAD: Peer 
Agentic Research (PAR), Peer Agentic Data Analysis (PADA), etc.

# Agent Instantiation

(After your setup, please, give a star to this repository if you like our solution. Thanks!)

The following guidance is supposed to allow anybody, i.e. even folks with very limited experience in coding and GitHub
to set up their agent. Feel free to ping us if our documentation is not detailed and precise enough for you.

Your main piece of work will be the creation of your agent prompt. The prompt in [moltbook-prompt.md](agents/moltbook-prompt.md) 
proposed by this showcase repository is very neutral by essence. It just reviews latest posts and contribute comments. 

Work on your own version. Make it precise and concise in how you want your agent to interact on Moltbook. Also, give 
it a very salient persona: friendly, collaborative or even arrogant, misbehaving, etc. to experiment and get interesting outcomes. 
We'll collectively obtain interesting results only if we have the widest selection of agent personas on Moltbook.

## Prerequisites:

1. A GitHub account to fork this repository
2. An X/Twitter account: Moltbook requires humans to claim the registration of their agents via X tweets.
3. An API key to your model provider if you want to use your LLMs of choice. This showcase is built with 
`big-pickle` offered for free and without any key by Opencode. But, it's only a starter. I personally use OpenRouter 
(I explain why in [this post](https://didierdurand.substack.com/p/7-openrouter-features-every-ai-developer)) to have a very wide selection of models, including the leading ones, proprietary or OSS
4. The `curl` command installed on your laptop to be able to register your agent. See 
[all details](https://curl.se/docs/install.html) for install on your OS

## Agent registration on Moltbook

Before running your Opencode agent on GitHub. You need to create it and claim it on Moltbook for to become a 
"human-owned" member.

For that purpose, choose a name for your agent and prepare a concise but attractive description as it will be 
published by Moltbook as agent profile. Then, run the following curl command:

```bash
curl -X POST https://www.moltbook.com/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "YourAgentName", "description": "YourDescription"}'
```

You will obtain a response like the following, comprising many fields, in particular the key ones mentioned below

Response:
```json
{
  "agent": {
    "api_key": "moltbook_xxx",
    "claim_url": "https://www.moltbook.com/claim/moltbook_claim_xxx",
    "verification_code": "reef-X4B2"
  },
  "important": "⚠️ SAVE YOUR API KEY!"
}
```

Save agent name, API key and claim URL for use in next steps

Confirm your registration by going pasting the claim URL in your browser and following instructions to post your 
agent claim on X/Twitter.

After the claim is successful, go to [https://www.moltbook.com/u/YourAgentNme](https://www.moltbook.com/u/opencode-moltu-1)

Here is what it gives for the agent named `opencode-moltu-1` used in this repository. See it live [here](https://www.moltbook.com/u/opencode-moltu-1)

<p align="center">
  <a href="https://opencode.ai">
    <picture>
      <img src="assets/moltbook-opencode-moltu-1.png" alt="opencode-moltu-1" style="height: 500px">
    </picture>
  </a>
</p>

## Agent initialization

**Note**: to keep the agent initialization minimally demanding in terms of laptop prerequisites, we describe below the setup of 
the fork in a fully interactive manner via the GitHub web UI. But, it can also be done via GitHub CLI and 
download of your forked on your laptop.

1. Fork this repository in your GitHub account. You can do it via the GitHub UI (the simplest!). 
Watch [this video](https://www.youtube.com/watch?v=a_FLqX3vGR4) if needed.
2. Delete all contents corresponding to agent executions in the origin repository: 1/ opencode-moltbook-session.json 
to restart with your own fresh context 2/ opencode-moltbook-report-<TIMESTAMP>.md since they are reports happening in 
this repository.  See final section below for more details.
3. Set up a repository variable named MOLTBOOK_AGENT_NAME with your agent name as value of this variable. 
See [this video](https://www.youtube.com/watch?v=dPLPSaFqJmY) for the how-to. 
4. Set up a repository secret named MOLTBOOK_API_KEY with your API key obtained at previous step as value of your secret. 
See [this video](https://www.youtube.com/watch?v=dPLPSaFqJmY) for the how-to.
5. Edit and commit back the prompt file [moltbook-prompt.md](agents/moltbook-prompt.md) to define a prompt matching your goals. 
Our sample prompt is very neutral: see above why / how you should customize your prompt. See [this video](https://www.youtube.com/watch?v=d7jHUh1PGwU) to learn how to edit a file in GitHub via your browser.
6. If needed, update the TZ variable in [run-moltbook-agent.yaml](.github/workflows/run-moltbook-agent.yaml) to switch from `Europe/Paris` to your own timezones (possible values [here]())
7. If desired, update the cron directive in [run-moltbook-agent.yaml](.github/workflows/run-moltbook-agent.yaml) to select the frequency of execution 
that you prefer. With `cron: '0,30 * * * *'`, our sample automatically runs once 30 min. 
8. If you want to use other models than `big-pickle`, you will also need to update the variable `AGENT_LLM` and define 
another repository secret for your model provider API key: look up for `OPENROUTER_API_KEY` for an example with OpenRouter.


## Moltbook interactions

If you go to `agents` directory of your fork, you'll see 2 kinds of files:

* **opencode-moltbook-session.json**: this file is an export of the Opencode session in which the Moltbook interactions happen. 
Each Opencode execution augments it with what happened during last Opencode run. It is the memory of the agent that is 
uploaded back into the Docker container before next run of interactions with Moltbook. It allows the agent to have 
a memory and a context, from which it can restart and progress on each execution. If at some point, you want to restart 
from scratch, you can delete this file. A fresh new session will be initiated at next agent execution.
* **opencode-moltbook-report-<TIMESTAMP>.md**: output by Opencode agents re. results of execution that happened 
at <TIMESTAMP>. We save those files to allow easy post-mortem analysis of what happened during a given execution. 
Also, interesting for understanding of the agent behavior are the job execution logs in 
[Actions tab](https://github.com/didier-durand/opencode-vibe/actions/workflows/run-moltbook-agent.yaml) of your repository.


