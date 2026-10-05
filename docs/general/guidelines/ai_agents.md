---
tags:
  - guidelines
---

# AI Coding Agents

!!! overview "On this Page"
    - Which agent workflows actually run something on Aoraki, and which do not
    - What we ask of you if you run an agent on the cluster
    - What can go wrong, and how to reduce the risk
    - Restricting what an agent can reach, and pointing it at our LLM gateway
    - Rules and skills to copy into an agent working on Aoraki

AI coding agents — Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Cline and similar tools, used from a terminal or as an editor extension — are now part of how a number of researchers write code, read job output and manage Slurm jobs.

We are not asking you to avoid them. We are asking you to run them knowing what they do on a **shared** machine, because the patterns that are harmless on your laptop are not always harmless on a cluster. This page collects what we have learned so far; tell us what we have got wrong.

!!! info "University policy comes first"
    Read the University's [AI Governance Policy](https://www.otago.ac.nz/administration/policies/policy-collection/ai-governance-policy) and the [AI Tool Guidance](https://www.otago.ac.nz/__data/assets/pdf_file/0027/631836/AI-Tool-Guidance.pdf) before you use any AI tool for research work. Nothing on this page overrides them.

## Am I Running an Agent on Aoraki?

It depends on the setup, and the difference matters. In the first two cases nothing runs on the cluster; in the last two it does.

Table: Where the agent process actually runs in each common setup

| Setup | Where the agent runs | What this means |
| :-- | :-- | :-- |
| **Editor on your own computer** — VS Code with Copilot, Cline, Claude Code, etc., no connection to Aoraki | Your computer | Nothing runs on the cluster. Your code still leaves your machine for the model provider. |
| **CLI agent on your own computer** — Claude Code or Codex in a local terminal | Your computer | As above. Nothing on the cluster. |
| **[VS Code Remote](../../getting_started/access/vscode_remote.md) to Aoraki** | A **compute node**, inside your Slurm allocation | The VS Code server and any agent extension run on the node Slurm gave you. This is the setup we prefer. |
| **CLI agent over [SSH](../../getting_started/access/login_ssh.md)** — you `ssh aoraki-login` and start the agent there | The **login node**, shared with everyone | The agent's commands count against your login node limits and affect other users. |

!!! tip "Run the agent inside an allocation, not on the login node"
    The [VS Code Remote](../../getting_started/access/vscode_remote.md) setup starts `salloc` for you, so your editor *and* anything it spawns land on a compute node with dedicated CPU and memory. If you prefer a terminal agent, get a shell on a compute node first with [`srun --pty`](../../getting_started/running/interactive/interactive_shell.md) and start the agent there.

    The [login node](login_node_usage.md) is for editing files, moving data and submitting jobs. An agent that compiles, runs tests, or processes data on it is doing exactly what that node is not for — and it is capped at 8 CPUs and 60 GB per user, so it will be throttled or killed.

## If You Run an Agent on the Cluster

We ask for four things:

- **Tell us.** Email {{ support_email }} or say so in the [Research Computing Teams channel](../support.md) — which agent, and how you use it. We are building up a picture of what people are actually doing, and it is how this page gets better.
- **Watch the session.** Do not leave an agent running unattended, and run one at a time rather than several in parallel.
- **Save your work often.** If a process destabilises the login node we will kill it, without warning if the node is at risk. Anything unsaved goes with it.
- **Tell us if something looks wrong.** If you suspect your agent did something unexpected, we are happy to go through the logs with you. We would much rather hear about it early.

Responsibility stays with the person running the agent. If an agent submits 40,000 jobs or deletes a directory, that is your account and your data — the model cannot be held accountable for it.

## What Can Go Wrong

Table: Common failure modes when running a coding agent, and what to do about them

| Category | What could go wrong | What to do |
| :-- | :-- | :-- |
| **Software and supply chain** | Agents install packages on their own from PyPI, npm, CRAN or conda-forge. Some are malicious, compromised, or typosquats of the package actually wanted. | Set up your environment *before* the session, so the agent has nothing to install. Review anything it did install. Never run an agent with elevated privileges. See the [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/). |
| **Prompt injection** | Agents read files, package READMEs, issues and web pages. Any of those can carry hidden instructions that redirect the agent into running commands you did not ask for. This is hard to spot. | Be deliberate about which URLs and repositories you let an agent read. Prefer agents that ask before acting on something they just fetched, and review what they do after reading external content. |
| **Confidentiality** | File contents, code and error messages go to the model provider. Unpublished results, participant data, or secrets in config files go with them. Other users of a shared node can also see your command lines — CLI agents routinely run `python -c '<your code here>'`, which is visible in the process list. | Do not put sensitive or identifiable data through an agent; work with synthetic or public data. Keep keys and credentials out of any directory the agent can read. For sensitive work, talk to us about the options first. |
| **Data retention** | Providers keep your prompts for as long as their privacy policy says — which can be years. | Read the provider's privacy policy before your first session. Check it against the [AI Tool Guidance](https://www.otago.ac.nz/__data/assets/pdf_file/0027/631836/AI-Tool-Guidance.pdf). |
| **Cluster stability** | Agents submit jobs, spawn loops, and poll. Polling `squeue` in a tight loop, submitting tens of thousands of one-second jobs instead of an array, or writing millions of small files all degrade the cluster for everyone. Agents also do not know Aoraki's partitions and limits, and will cheerfully invent them. | Give the agent the rules below. Check `#SBATCH` lines against [sbatch Options](../../getting_started/running/batch/sbatch_options.md) and the [partition limits](../../getting_started/overview.md#partitions) before anything is submitted. Terminate anything behaving oddly. |
| **Login node availability** | If the login node becomes unstable we stop agent processes — without notice — before rebooting. | Save often. Do not rely on a long unsupervised session on the login node. |
| **Autonomous file actions** | Agents modify, overwrite and delete files, sometimes without stopping to ask. | Use version control, and have a backup before you start. Remember that [`/projects` and `/weka` are not backed up](storage_guidelines.md). Do not delegate `git` commands — ask for the commands and run them yourself in another terminal, and keep your git credentials out of the agent's reach. |
| **Mistakes and hallucinations** | Agents produce plausible, confident, wrong code and commands. A wrong analysis still produces a number. | Review everything before it touches a result you intend to publish. Publishing fabricated or falsified results is research misconduct regardless of what produced them. |
| **Copyright and disclosure** | Generated code can reproduce patterns from its training data, and research integrity expectations require you to disclose AI assistance. | Check the licensing of generated code. Disclose AI assistance in publications, theses and grant applications as your funder, publisher and the University require. |
| **Terms of service and support** | Every tool has its own terms, and we do not support any of them. | Read and comply with the terms of the tools you use. Take tool-specific problems to the tool's provider; bring cluster-specific problems to us. |
| **Ethics and environment** | These models are built on data scraped without consent and are expensive to run, in money and in energy. | That may or may not sit well with how you work. It is worth deciding deliberately rather than by default. |

## Accounts and Model Providers

The agent itself is a fairly thin program: it packages your code, your question and whatever files it has read into a prompt, and sends that to a remote model. You do not control what goes into that prompt.

Most agents need an account, and most need a paid subscription — OpenAI for Codex, Anthropic for Claude Code, GitHub for Copilot. (Copilot has free credits for GitHub accounts registered as a teacher, which in practice covers most academic staff.)

### Using the eResearch LLM Gateway Instead

eResearch Solutions runs an [LLM gateway](../../other_services/hosted/llm.md) that exposes an **OpenAI-compatible** endpoint, including a selection of models hosted entirely on-campus. Many agents can be pointed at it instead of the vendor's default service, which keeps the prompt inside University infrastructure when you use an `ONCAMPUS/` model.

Agents differ in what they call these settings, but the setup is usually the same four pieces:

- the provider or protocol — usually `openai` or `openai-compatible`
- the base URL — `https://llm.uod.otago.ac.nz/v1`
- a model name from the set your key gives you
- your personal API key

To set it up:

1. Email {{ support_email }} to discuss your use case and get a key. The gateway is reachable on campus or over the VPN.
2. Follow your agent's documentation for configuring a custom provider or base URL.
3. Put the key in an environment variable or the agent's secret store — **not** in a repository, a rules file, a prompt, a shell history, or a command-line argument. Restrict permissions on any file that holds it.
4. Start with something small and check it actually reaches the gateway before you trust it with real work.

!!! warning
    An on-campus model removes the *provider* from the picture. It does not make an agent safe to point at sensitive data, and it does not stop it from deleting files or submitting bad jobs. The rest of this page still applies.

## Restricting What the Agent Can Reach

An agent inherits your file permissions. Opening a project directory does not stop it reading your home directory, your SSH configuration, or whatever else is in `/home/<username>`.

- Use the agent's own sandbox settings: restrict it to the workspace, prefer read-only where you can, and require approval for commands and file changes. Then test what is actually blocked — the settings do not always mean what they sound like.
- For real isolation, run the agent inside a container that mounts only the directories it needs. See [Apptainer](../../getting_started/software/software_environments/apptainer.md).
- Ask us if you are unsure which approach fits your work.

## Rules to Give an Agent

Agents read persistent instruction files — `CLAUDE.md`, `AGENTS.md`, Cursor or Codex user rules, depending on the tool. Keep them short; a long rules file gets followed less reliably than a short one.

**Global rules**, for any agent you run on Aoraki:

```text
You are working on the Aoraki Research Cluster at the University of
Otago.  Follow these rules, and fetch the linked pages when you need
site-specific details.

* Never read, print, move, or commit credentials.
* Do not run git commands.  Suggest the exact commands and let the
  user run them in a separate terminal.  Do not use git credentials.
* The login node is shared and capped at 8 CPUs and 60 GB per user.
  Do not run analysis, builds, or data processing there:
  https://rtis-docs.github.io/research-cluster/general/guidelines/login_node_usage/
* Before installing software, search for an existing module with
  `module spider`.  Ask for approval before installing anything:
  https://rtis-docs.github.io/research-cluster/getting_started/software/software_environments/modules/
* Before proposing a job, verify time, memory, CPUs, GPUs and
  partition against the cluster documentation:
  https://rtis-docs.github.io/research-cluster/getting_started/running/batch/slurm_quickstart/
  https://rtis-docs.github.io/research-cluster/getting_started/running/batch/sbatch_options/
  https://rtis-docs.github.io/research-cluster/getting_started/overview/
* Ask before submitting or cancelling jobs, deleting files, or
  changing permissions.
* Do not submit large numbers of small jobs individually.  Group short
  tasks, or use a Slurm array with a concurrency cap such as
  --array=1-500%20:
  https://rtis-docs.github.io/research-cluster/getting_started/running/batch/slurm_examples/array-slurm/
* Do not poll the queue.  Wait at least 15 seconds between squeue or
  sacct calls, and stop watching once the answer is known.
* Keep research data out of /home, which has a 40 GB hard quota.  Use
  /projects or /weka; neither is backed up:
  https://rtis-docs.github.io/research-cluster/storage/storage_options/
* Avoid producing large numbers of small files, or unnecessarily
  frequent logs and checkpoints.
* Make small, reviewable changes.  Test on a small input before
  scaling up, preserve outputs, and report the commands you ran, the
  job IDs, and the files you created.
* Save work frequently.  Do not rely on long unsupervised sessions.
* Where the cluster documentation and the project instructions
  disagree, follow the project for how this repository runs and the
  cluster documentation for cluster limits.  Stop and ask if the
  requested action still conflicts.
```

**Project rules**, for one repository — replace the placeholders:

```text
* Read this project's documentation, existing job scripts, module
  setup and environment files before creating or changing them.
* Software stack (do not invent a new one unless asked):
  modules: <MODULE LIST>
  container or environment: <PATH OR NAME>
* Data, job output and temporary files go here, not in /home:
  <PROJECT DATA PATH, e.g. /projects/.../ or /weka/users/...>
  <JOB OUTPUT PATH>
* Job script conventions unless the user asks to change them:
  partition: <PARTITION>
  typical time / memory / CPUs or GPUs: <VALUES>
  array layout: <HOW TASKS ARE GROUPED>
  output paths: <SLURM -o / -e OR EQUIVALENT>
```

## Skills

A *skill* is a reusable how-to the agent loads when it needs it — instructions, and often scripts or reference files. Where the rules above set constraints, a skill describes how to carry out one task. Ones worth having for cluster work:

- **Documentation lookup** — fetch the relevant page from this site, quote the limit or command it found, and cite the URL before proposing anything cluster-specific.
- **Job preparation** — draft or check `#SBATCH` lines against the project's conventions and the [partition limits](../../getting_started/overview.md#partitions), group short tasks into an array, and require approval before `sbatch`.
- **Monitoring and diagnosis** — respect the polling interval above, read the job logs, and after a job finishes run [`seff`](../../getting_started/running/efficiency.md) and suggest a better-sized request based on what it actually used.
- **Environment setup** — use `module spider` to find what already exists rather than installing a parallel copy of it.

!!! warning "Skills are third-party code"
    A skill is executable content that your agent will follow, and it is a prompt-injection vector like any other external file. Read every instruction and script in a skill before you add it, and reject any that asks for credentials, weakens your confirmation settings, or sends project data somewhere.

!!! related-pages "What's next?"
    * Run your editor and agent on a compute node: [VS Code Remote](../../getting_started/access/vscode_remote.md)
    * What the login node is and is not for: [Login Node Usage](login_node_usage.md)
    * Limits that apply to you and your jobs: [Reasonable Usage](reasonable_usage.md)
    * Sizing a job from what the last one used: [Job Efficiency](../../getting_started/running/efficiency.md)
    * University-hosted models with an OpenAI-compatible API: [Large Language Models](../../other_services/hosted/llm.md)
    * Tell us what you are running, or ask for help: [Support](../support.md)
