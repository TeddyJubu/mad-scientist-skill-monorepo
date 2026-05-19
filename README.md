# Mad Scientist Skill Monorepo

<p align="center">
  <strong>204 standalone Mad Scientist agent skills, flattened into individually installable packages.</strong>
</p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/skills-204-111827?style=for-the-badge">
  <img alt="Packages" src="https://img.shields.io/badge/packages-204-7c3aed?style=for-the-badge">
  <img alt="Workspace" src="https://img.shields.io/badge/workspace-pnpm-2563eb?style=for-the-badge">
  <img alt="Layout" src="https://img.shields.io/badge/layout-flat-059669?style=for-the-badge">
</p>

---

## What This Is

This repository is a flat monorepo of standalone `SKILL.md` packages. Every skill has its own package identity under `packages/<skill-slug>/`; there are no category folders and no category grouping.

Each package preserves the skill's instructions and supporting files such as scripts, references, examples, workflows, tests, templates, and assets.

## AI Agent Install Guide

Use this repository when your agent expects a flat directory of independent skills. This is the cleanest install target for runtimes that do not understand categories.

### 1. Clone

```bash
git clone https://github.com/TeddyJubu/mad-scientist-skill-monorepo.git
cd mad-scientist-skill-monorepo
```

### 2. Validate Before Loading

```bash
test "$(find packages -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" = "204"
test "$(find packages -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')" = "204"
test "$(find packages -name SKILL.md | wc -l | tr -d ' ')" = "204"

python3 - <<'PY'
from pathlib import Path
import json, re
names = set()
bad = []
for package_dir in Path("packages").iterdir():
    if not package_dir.is_dir():
        continue
    skill = package_dir / "SKILL.md"
    manifest = package_dir / "package.json"
    if not skill.exists() or not manifest.exists():
        bad.append(str(package_dir))
        continue
    data = json.loads(manifest.read_text())
    package_name = data.get("name", "")
    if not re.fullmatch(r"@mad-scientist-skills/[a-z0-9][a-z0-9-]*", package_name):
        bad.append(f"bad package name: {manifest}")
    if package_name in names:
        bad.append(f"duplicate package: {package_name}")
    names.add(package_name)
    text = skill.read_text(errors="replace")
    if not text.startswith("---") or not re.search(r"^name:\s*.+", text, re.M) or not re.search(r"^description:\s*.+", text, re.M):
        bad.append(f"bad frontmatter: {skill}")
if bad:
    raise SystemExit("\n".join(bad))
print("Validated 204 standalone skill packages")
PY
```

### 3. Install Into An Agent Skill Root

Set `AGENT_SKILLS_ROOT` to the directory your agent scans. If unset, the commands use the common Hermes path.

```bash
export AGENT_SKILLS_ROOT="${AGENT_SKILLS_ROOT:-$HOME/.hermes/skills}"
mkdir -p "$AGENT_SKILLS_ROOT"

for package_dir in packages/*; do
  test -f "$package_dir/SKILL.md" || continue
  skill_id="$(basename "$package_dir")"
  rsync -a --delete \
    --exclude ".env" \
    --exclude "*.env" \
    --exclude "__pycache__" \
    --exclude "*.pyc" \
    --exclude "*.log" \
    --exclude ".DS_Store" \
    "$package_dir/" "$AGENT_SKILLS_ROOT/$skill_id/"
done
```

Then point the agent at:

```text
$AGENT_SKILLS_ROOT
```

### 4. Install Or Inspect One Skill

```bash
export AGENT_SKILLS_ROOT="${AGENT_SKILLS_ROOT:-$HOME/.hermes/skills}"
rsync -a --delete packages/weather/ "$AGENT_SKILLS_ROOT/weather/"
sed -n '1,120p' "$AGENT_SKILLS_ROOT/weather/SKILL.md"
```

### 5. Load Behavior For Agents

- Treat every `packages/<skill-slug>/` as a separate skill identity.
- Use the folder slug for filesystem identity and frontmatter `name` for runtime display or command identity.
- Read `package.json` for install metadata only; the operational source of truth is `SKILL.md`.
- Read local `references/`, `scripts/`, `templates/`, `tests/`, and `assets/` only when that skill is selected.
- Do not run helper scripts during install.
- Keep live credentials in local `.env` files outside git.

## Layout

```text
mad-scientist-skill-monorepo/
├── package.json
├── pnpm-workspace.yaml
└── packages/
    ├── agent-browser/
    │   ├── SKILL.md
    │   └── package.json
    ├── weather/
    │   ├── SKILL.md
    │   └── package.json
    └── ...
```

## Developer Quick Start

```bash
git clone https://github.com/TeddyJubu/mad-scientist-skill-monorepo.git
cd mad-scientist-skill-monorepo
pnpm install
pnpm list
```

Inspect one skill:

```bash
cd packages/weather
sed -n '1,120p' SKILL.md
```

## Package Index

| Skill | Package | Description |
|---|---|---|
| [`agent-browser`](./packages/agent-browser) | `@mad-scientist-skills/agent-browser` | A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. |
| [`agentmail`](./packages/agentmail) | `@mad-scientist-skills/agentmail` | Give the agent its own dedicated email inbox via AgentMail. Send, receive, and manage email autonomously using agent-owned email addresses (e.g. hermes-agent@agentmail.to). |
| [`agentmail-productivity`](./packages/agentmail-productivity) | `@mad-scientist-skills/agentmail-productivity` | agentmail lets the user create and manage dedicated email inboxes for AI agents, send and receive emails programmatically, and handle email-based workflows with webhooks and real-time events, which is useful when they need an agent to have its own email identity for outreach, notifications, or handling incoming email without relying on traditional personal email accounts. |
| [`airtable`](./packages/airtable) | `@mad-scientist-skills/airtable` | Airtable REST API via curl. Records CRUD, filters, upserts. |
| [`apify`](./packages/apify) | `@mad-scientist-skills/apify` | Run any Apify Actor to scrape web data (Instagram, TikTok, Reddit, Twitter, etc). Handles Actor discovery, quality filtering, probe testing, batched execution, and result collection. Use when user asks to scrape/crawl/extract data from websites or social media platforms, or mentions Apify directly. |
| [`apify-actor-finder`](./packages/apify-actor-finder) | `@mad-scientist-skills/apify-actor-finder` | Finds the best Apify actor for a web scraping or data extraction task, runs it via the Apify API, and delivers the results as a CSV file. Use this skill whenever a user wants to scrape a website or extract data from any platform (e.g. Google Maps, Twitter/X, Instagram, Facebook, TikTok, LinkedIn, Amazon, real estate sites, etc.). This skill handles the full workflow: finding the actor, running it, and returning results. |
| [`apify-mcp`](./packages/apify-mcp) | `@mad-scientist-skills/apify-mcp` | Enhanced Apify integration using mcpc (Model Context Protocol CLI). Provides dynamic actor discovery, direct tool calling, and better error handling via persistent MCP sessions. Use when you need to search, inspect, run, or monitor Apify actors with the full power of the MCP protocol. |
| [`apollo-find`](./packages/apollo-find) | `@mad-scientist-skills/apollo-find` | Search for B2B contacts and companies using the Apollo.io API. Use this skill when the user wants to find leads, prospects, or business contacts — including filtering by job title, seniority, location, company size, revenue, industry, or technology stack. Also handles company/organization search and people enrichment (emails/phones). Triggers on phrases like "find contacts", "search Apollo", "find leads", "look up companies", "B2B prospecting", "find [job title] at [company type]", "enrich a contact", or any Apollo.io data request. |
| [`apple-notes`](./packages/apple-notes) | `@mad-scientist-skills/apple-notes` | Manage Apple Notes via memo CLI: create, search, edit. |
| [`apple-reminders`](./packages/apple-reminders) | `@mad-scientist-skills/apple-reminders` | Apple Reminders via remindctl: add, list, complete. |
| [`architecture-diagram`](./packages/architecture-diagram) | `@mad-scientist-skills/architecture-diagram` | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| [`arxiv`](./packages/arxiv) | `@mad-scientist-skills/arxiv` | Search arXiv papers by keyword, author, category, or ID. |
| [`ascii-art`](./packages/ascii-art) | `@mad-scientist-skills/ascii-art` | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| [`ascii-video`](./packages/ascii-video) | `@mad-scientist-skills/ascii-video` | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| [`audiocraft-audio-generation`](./packages/audiocraft-audio-generation) | `@mad-scientist-skills/audiocraft-audio-generation` | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| [`axolotl`](./packages/axolotl) | `@mad-scientist-skills/axolotl` | Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO). |
| [`baoyu-comic`](./packages/baoyu-comic) | `@mad-scientist-skills/baoyu-comic` | Knowledge comics: educational, biography, tutorial. |
| [`baoyu-infographic`](./packages/baoyu-infographic) | `@mad-scientist-skills/baoyu-infographic` | Infographics: 21 layouts x 21 styles. |
| [`batchdata-skip-trace`](./packages/batchdata-skip-trace) | `@mad-scientist-skills/batchdata-skip-trace` | batchdata-skip-trace lets the user upload or work from a property or owner list and quickly find likely contact details tied to those records, such as phone numbers, email addresses, mailing addresses, and related ownership signals, so they can move faster on outreach, lead qualification, and list cleanup without doing manual people-search work one record at a time. |
| [`beautiful-websites`](./packages/beautiful-websites) | `@mad-scientist-skills/beautiful-websites` | Find local businesses with outdated websites, redesign them with premium single-file HTML sites, and deploy them to Vercel. Use when the user wants to generate proof-of-work redesigns for outreach, create portfolio pieces from real business sites, or run the full pipeline (scrape → qualify → redesign → deploy) for a specific niche and city. Triggers on phrases like "beautiful websites", "redesign local business sites", "run the pipeline for [niche] in [city]", or any request to scrape, qualify, redesign, and deploy business websites. |
| [`blogwatcher`](./packages/blogwatcher) | `@mad-scientist-skills/blogwatcher` | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. |
| [`blotato-text-poster`](./packages/blotato-text-poster) | `@mad-scientist-skills/blotato-text-poster` | blotato-text-poster lets the user publish text-based social content through Blotato, making it useful for pushing written posts, captions, short updates, promotional copy, or repurposed text assets out to connected social channels without having to manually open each platform and post them one by one. |
| [`bob`](./packages/bob) | `@mad-scientist-skills/bob` | bob lets the user skip trace a property address to find owner names, phone numbers (with DNC/TCPA compliance flags), email addresses, alternate mailing addresses, and property details via the BatchData API v3, making it useful when they need to move fast on a deal, qualify a lead, or run outreach without doing manual people-search work one record at a time. |
| [`brave-search`](./packages/brave-search) | `@mad-scientist-skills/brave-search` | brave-search lets the user search the web and extract content via the Brave Search API, which is useful when they need quick answers, fact checks, documentation lookups, or want to pull structured content from websites without running a full browser or web crawler. |
| [`browser-use-cloud`](./packages/browser-use-cloud) | `@mad-scientist-skills/browser-use-cloud` | Use Browser Use Cloud API v3 for managed AI browser automation, live browser sessions, screenshots, web research, form workflows, authentication profiles, file workspaces, and OpenClaw/Hermes browser tasks. Trigger whenever Charles asks Browser Use, cloud browser automation, web task agents, AI browser API, live browser preview, profile sync, or CDP stealth browser infrastructure. |
| [`browser-use-cloud-openclaw`](./packages/browser-use-cloud-openclaw) | `@mad-scientist-skills/browser-use-cloud-openclaw` | Use Browser Use Cloud API v3 for managed AI browser automation, live browser sessions, screenshots, web research, form workflows, authentication profiles, file workspaces, and OpenClaw/Hermes browser tasks. Trigger whenever Charles asks Browser Use, cloud browser automation, web task agents, AI browser API, live browser preview, profile sync, or CDP stealth browser infrastructure. |
| [`census-data`](./packages/census-data) | `@mad-scientist-skills/census-data` | Fetch demographic, economic, and population data from the U.S. Census Bureau API. Use this skill when you need population statistics, housing data, business patterns, income/poverty estimates, or any U.S. government statistical data at national, state, county, metro, tract, or block group levels. |
| [`claude-code`](./packages/claude-code) | `@mad-scientist-skills/claude-code` | Delegate coding to Claude Code CLI (features, PRs). |
| [`claude-design`](./packages/claude-design) | `@mad-scientist-skills/claude-design` | Design one-off HTML artifacts (landing, deck, prototype). |
| [`clip`](./packages/clip) | `@mad-scientist-skills/clip` | OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. Use for image search, content moderation, or vision-language tasks without fine-tuning. Best for general-purpose image understanding. |
| [`code-review`](./packages/code-review) | `@mad-scientist-skills/code-review` | Guidelines for performing thorough code reviews with security and quality focus |
| [`codebase-inspection`](./packages/codebase-inspection) | `@mad-scientist-skills/codebase-inspection` | Inspect codebases w/ pygount: LOC, languages, ratios. |
| [`codex`](./packages/codex) | `@mad-scientist-skills/codex` | Delegate coding to OpenAI Codex CLI (features, PRs). |
| [`comfyui`](./packages/comfyui) | `@mad-scientist-skills/comfyui` | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycle and direct REST/WebSocket API for execution. |
| [`content-repurposer`](./packages/content-repurposer) | `@mad-scientist-skills/content-repurposer` | Content Repurposer lets the user transform existing content into multiple new formats, angles, and platform-specific assets, helping them stretch one original piece of content into a broader publishing system that can feed email, social, video clips, carousels, captions, and promotional material without starting from scratch each time. |
| [`content-repurposing-engine`](./packages/content-repurposing-engine) | `@mad-scientist-skills/content-repurposing-engine` | content-repurposing-engine lets the user take one core piece of content, like a video, podcast, interview, newsletter, or long-form post, and spin it into multiple smaller assets for different platforms, such as captions, clips, tweets, carousels, emails, hooks, and short-form posts, so a single idea can produce a full content stack instead of being used once and forgotten. |
| [`copywriting`](./packages/copywriting) | `@mad-scientist-skills/copywriting` | copywriting lets the user create clear, persuasive written content for sales pages, ads, emails, landing pages, offer descriptions, social posts, and follow-up messages, with messaging shaped to match the audience, goal, and platform so the final copy is not just polished, but built to get attention, generate response, and move people toward a specific action. |
| [`daily-eod-report`](./packages/daily-eod-report) | `@mad-scientist-skills/daily-eod-report` | Generate the daily end-of-day agent report summarizing all agent activity, system tasks, and files created. Runs at 5 PM ET daily via cron. |
| [`data-infographic-generator`](./packages/data-infographic-generator) | `@mad-scientist-skills/data-infographic-generator` | Generate data-rich comparison infographics (9:16 mobile or 16:9 landscape) with verified research data. Used for AI model comparisons, product specs, pricing tables, and any structured data presentation. |
| [`debugging-hermes-tui-commands`](./packages/debugging-hermes-tui-commands) | `@mad-scientist-skills/debugging-hermes-tui-commands` | Debug Hermes TUI slash commands: Python, gateway, Ink UI. |
| [`design-md`](./packages/design-md) | `@mad-scientist-skills/design-md` | Author/validate/export Google's DESIGN.md token spec files. |
| [`discord`](./packages/discord) | `@mad-scientist-skills/discord` | discord lets the user control Discord from an AI agent, sending messages, reactions, stickers, polls, and files; managing threads, pins, and searches; fetching permissions and member or channel info; and handling moderation actions in DMs or channels, which is useful when they need to manage a Discord community, run a bot, or automate engagement without being at their keyboard. |
| [`docker-management`](./packages/docker-management) | `@mad-scientist-skills/docker-management` | Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization. |
| [`dogfood`](./packages/dogfood) | `@mad-scientist-skills/dogfood` | Systematic exploratory QA testing of web applications — find bugs, capture evidence, and generate structured reports |
| [`dspy`](./packages/dspy) | `@mad-scientist-skills/dspy` | DSPy: declarative LM programs, auto-optimize prompts, RAG. |
| [`enhancor`](./packages/enhancor) | `@mad-scientist-skills/enhancor` | enhancor lets the user generate any type of video through a guided, conversational workflow using the Seedance 2.0 / Enhancor API, asking the right questions in the right order and delivering the finished video to Telegram so they can create marketing clips, promotional content, or visual assets without navigating complex video production tools. |
| [`evaluating-llms-harness`](./packages/evaluating-llms-harness) | `@mad-scientist-skills/evaluating-llms-harness` | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| [`excalidraw`](./packages/excalidraw) | `@mad-scientist-skills/excalidraw` | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| [`fal-ai-video-generation`](./packages/fal-ai-video-generation) | `@mad-scientist-skills/fal-ai-video-generation` | Generate short-form AI videos (text-to-video) using fal.ai — Kling 1.6 and other models. Use when Charles asks for AI-generated video content, short-form clips, Reels, Shorts, or TikToks built from scratch without filming. FAL_KEY is available in /root/.openclaw/.openclaw/.env. |
| [`file-delivery`](./packages/file-delivery) | `@mad-scientist-skills/file-delivery` | Complete file delivery system — outbound (VPS→Telegram) and inbound (Telegram→VPS or URL→VPS). Always use this when producing or receiving files. |
| [`filebrowser-deploy`](./packages/filebrowser-deploy) | `@mad-scientist-skills/filebrowser-deploy` | Deploy filebrowser (web-based file manager) with HTTPS via Cloudflare tunnel on Charles' server |
| [`find-nearby`](./packages/find-nearby) | `@mad-scientist-skills/find-nearby` | Find nearby places (restaurants, cafes, bars, pharmacies, etc.) using OpenStreetMap. Works with coordinates, addresses, cities, zip codes, or Telegram location pins. No API keys needed. |
| [`findmy`](./packages/findmy) | `@mad-scientist-skills/findmy` | Track Apple devices/AirTags via FindMy.app on macOS. |
| [`fine-tuning-with-trl`](./packages/fine-tuning-with-trl) | `@mad-scientist-skills/fine-tuning-with-trl` | TRL: SFT, DPO, PPO, GRPO, reward modeling for LLM RLHF. |
| [`firecrawl`](./packages/firecrawl) | `@mad-scientist-skills/firecrawl` | firecrawl lets the user scrape, crawl, and map websites into clean markdown, which is useful when they need to extract content from pages, audit site structures, build knowledge bases from web sources, or feed structured web content into AI workflows without broken HTML or layout artifacts. |
| [`firehose`](./packages/firehose) | `@mad-scientist-skills/firehose` | firehose lets the user monitor the web in real-time by creating Lucene query rules that track specific keywords, domains, or page types and stream matching results via Server-Sent Events, which is useful when they want to track brand mentions, competitor activity, news alerts, or website changes as they happen instead of polling manually. |
| [`fish-audio-tts`](./packages/fish-audio-tts) | `@mad-scientist-skills/fish-audio-tts` | fish-audio-tts lets the user convert text into natural-sounding speech using the Fish Audio API, which is useful for creating voiceovers, audio content, or AI narration without needing a recording studio or voice actor. |
| [`frontend-design`](./packages/frontend-design) | `@mad-scientist-skills/frontend-design` | Expert frontend design guidelines for creating beautiful, modern UIs. Use when building landing pages, dashboards, or any user interface. |
| [`gemini-image-editor`](./packages/gemini-image-editor) | `@mad-scientist-skills/gemini-image-editor` | Edit, enhance, remove objects, change backgrounds, and transform images using Google AI Studio Gemini Nano Banana Pro (Imagen 3). Use when you need to edit existing images, remove backgrounds, swap objects, change lighting, add/remove elements, or apply artistic transformations. |
| [`gguf-quantization`](./packages/gguf-quantization) | `@mad-scientist-skills/gguf-quantization` | GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing flexible quantization from 2-8 bit without GPU requirements. |
| [`gif-search`](./packages/gif-search) | `@mad-scientist-skills/gif-search` | Search/download GIFs from Tenor via curl + jq. |
| [`github-auth`](./packages/github-auth) | `@mad-scientist-skills/github-auth` | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| [`github-code-review`](./packages/github-code-review) | `@mad-scientist-skills/github-code-review` | Review PRs: diffs, inline comments via gh or REST. |
| [`github-issues`](./packages/github-issues) | `@mad-scientist-skills/github-issues` | Create, triage, label, assign GitHub issues via gh or REST. |
| [`github-pr-workflow`](./packages/github-pr-workflow) | `@mad-scientist-skills/github-pr-workflow` | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| [`github-repo-management`](./packages/github-repo-management) | `@mad-scientist-skills/github-repo-management` | Clone/create/fork repos; manage remotes, releases. |
| [`gmail-unread-autodraft`](./packages/gmail-unread-autodraft) | `@mad-scientist-skills/gmail-unread-autodraft` | gmail-unread-autodraft lets the user scan their Gmail inbox for unread messages and automatically create draft replies on each thread on a schedule, which is useful when they want to acknowledge emails, stay top-of-mind with contacts, or maintain an inbox-zero workflow without manually typing responses to every message. |
| [`godmode`](./packages/godmode) | `@mad-scientist-skills/godmode` | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. |
| [`gog`](./packages/gog) | `@mad-scientist-skills/gog` | gog lets the user interact with Google Workspace — Gmail, Calendar, Drive, Contacts, Sheets, and Docs — from the command line, which is useful when they want to manage emails, schedule meetings, access files, or automate Google workflows without opening a browser or switching between apps. |
| [`gohighlevel-api`](./packages/gohighlevel-api) | `@mad-scientist-skills/gohighlevel-api` | gohighlevel-api lets the user interact with their GoHighLevel CRM account programmatically using plain-language prompts, managing contacts, opportunities, appointments, conversations, workflows, payments, invoices, webhooks, social media posts, forms, surveys, users, and location settings, which is useful when they want to automate CRM tasks, sync leads, or build custom workflows without navigating the GHL UI manually. |
| [`google-drive-image-upload`](./packages/google-drive-image-upload) | `@mad-scientist-skills/google-drive-image-upload` | google-drive-image-upload lets the user automatically upload generated images to Charles's Google Drive folder for permanent backup, which is useful when they want to preserve visual assets, keep a centralized media library, or ensure important images are never lost if local storage or Telegram messages get cleared. |
| [`google-workspace`](./packages/google-workspace) | `@mad-scientist-skills/google-workspace` | Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration via Python. Uses OAuth2 with automatic token refresh. No external binaries needed — runs entirely with Google's Python client libraries in the Hermes venv. |
| [`gpt-image-2`](./packages/gpt-image-2) | `@mad-scientist-skills/gpt-image-2` | gpt-image-2 lets the user generate original images or edit existing ones using AI, which is useful for marketing graphics, concept visuals, branded content, ad creatives, mockups, thumbnails, and stylized scene creation when they need a fast way to turn an idea, prompt, or reference image into a finished visual asset. |
| [`graphic-design`](./packages/graphic-design) | `@mad-scientist-skills/graphic-design` | Support design understanding from basic visuals to professional production and theory. |
| [`grpo-rl-training`](./packages/grpo-rl-training) | `@mad-scientist-skills/grpo-rl-training` | Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training |
| [`guidance`](./packages/guidance) | `@mad-scientist-skills/guidance` | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework |
| [`healthcheck`](./packages/healthcheck) | `@mad-scientist-skills/healthcheck` | Track water and sleep with JSON file storage |
| [`heartmula`](./packages/heartmula) | `@mad-scientist-skills/heartmula` | HeartMuLa: Suno-like song generation from lyrics + tags. |
| [`hermes-agent`](./packages/hermes-agent) | `@mad-scientist-skills/hermes-agent` | Configure, extend, or contribute to Hermes Agent. |
| [`hermes-agent-setup`](./packages/hermes-agent-setup) | `@mad-scientist-skills/hermes-agent-setup` | Help users configure Hermes Agent — CLI usage, setup wizard, model/provider selection, tools, skills, voice/STT/TTS, gateway, and troubleshooting. Use when someone asks to enable features, configure settings, or needs help with Hermes itself. |
| [`hermes-agent-skill-authoring`](./packages/hermes-agent-skill-authoring) | `@mad-scientist-skills/hermes-agent-skill-authoring` | Author in-repo SKILL.md: frontmatter, validator, structure. |
| [`hermes-multi-agent-telegram`](./packages/hermes-multi-agent-telegram) | `@mad-scientist-skills/hermes-multi-agent-telegram` | Generic how-to for spinning up multi-agent Telegram setups using Hermes profiles. NOT applicable to Charles. Charles's sub-agents (Mark, Eric, Bob, Michael, Tammie) are SKILLS Hermes loads in-process — they have never had separate Telegram bots on the Hermes side. Do not propose @BotFather workflows for Charles. |
| [`hermes-workspace-setup`](./packages/hermes-workspace-setup) | `@mad-scientist-skills/hermes-workspace-setup` | Connect and troubleshoot Hermes Workspace (web UI at port 3001) to its Hermes Agent backend (API server at port 8642). Use when the dashboard shows "Connecting to Hermes Agent..." or when the enhanced /api/* endpoints are missing. |
| [`heygen-avatar-video`](./packages/heygen-avatar-video) | `@mad-scientist-skills/heygen-avatar-video` | heygen-avatar-video lets the user generate AI avatar talking-head videos using Charles Blair's custom HeyGen avatar, which is useful when they want to create UGC-style content for TikTok, Reels, or YouTube without filming, produce consistent on-brand video content at scale, or quickly turn a script into a finished talking-head video. |
| [`himalaya`](./packages/himalaya) | `@mad-scientist-skills/himalaya` | Himalaya CLI: IMAP/SMTP email from terminal. |
| [`homedepot-repair-estimator`](./packages/homedepot-repair-estimator) | `@mad-scientist-skills/homedepot-repair-estimator` | homedepot-repair-estimator lets the user turn property photos plus basic room measurements into a contractor-style repair estimate that recommends specific Home Depot materials, calculates likely quantities, shows pricing, explains why each product was chosen, totals the material cost, and packages the result into a usable report for rehabs, buy-box decisions, or seller conversations. |
| [`hr`](./packages/hr) | `@mad-scientist-skills/hr` | hr lets the user run a complete hiring intelligence system for founders who want to post jobs, screen candidates, and manage Upwork projects without spending hours on recruiting, which is useful when they need to find talent, evaluate applicants, or run an HR workflow powered by AI instead of manual HR work. |
| [`hr-hiring`](./packages/hr-hiring) | `@mad-scientist-skills/hr-hiring` | HR workflow for creating optimized Upwork job posts, saving them to Notion, and evaluating applicant files from Google Drive. Use this skill when the user wants to hire for a new role, post a job on Upwork, or evaluate candidates for a job. |
| [`huggingface-hub`](./packages/huggingface-hub) | `@mad-scientist-skills/huggingface-hub` | HuggingFace hf CLI: search/download/upload models, datasets. |
| [`humanizer`](./packages/humanizer) | `@mad-scientist-skills/humanizer` | Humanize text: strip AI-isms and add real voice. |
| [`ideation`](./packages/ideation) | `@mad-scientist-skills/ideation` | Generate project ideas via creative constraints. |
| [`image-editing`](./packages/image-editing) | `@mad-scientist-skills/image-editing` | Correct workflow for editing existing images on Hermes — AI-powered edits (Gemini Imagen 3) and PIL-based targeted edits (text/date swaps, logo overlays). For generating new images from scratch, use gpt-image-2 instead. |
| [`imessage`](./packages/imessage) | `@mad-scientist-skills/imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| [`instagram-carousel-authority`](./packages/instagram-carousel-authority) | `@mad-scientist-skills/instagram-carousel-authority` | instagram-carousel-authority lets the user turn a topic, offer, or business message into a strategic Instagram carousel built for reach, saves, shares, and authority-building, including the hook, slide structure, teaching angle, design direction, and caption strategy needed to make the post feel like a serious piece of content instead of random social filler. |
| [`jupyter-live-kernel`](./packages/jupyter-live-kernel) | `@mad-scientist-skills/jupyter-live-kernel` | Iterative Python via live Jupyter kernel (hamelnb). |
| [`kanban-orchestrator`](./packages/kanban-orchestrator) | `@mad-scientist-skills/kanban-orchestrator` | Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do the work yourself" rule and the basic lifecycle are auto-injected into every kanban worker's system prompt; this skill is the deeper playbook when you're specifically playing the orchestrator role. |
| [`kanban-worker`](./packages/kanban-worker) | `@mad-scientist-skills/kanban-worker` | Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker's system prompt as KANBAN_GUIDANCE (from agent/prompt_builder.py); this skill is what you load when you want deeper detail on specific scenarios. |
| [`landglide-lookup`](./packages/landglide-lookup) | `@mad-scientist-skills/landglide-lookup` | landglide-lookup lets the user search a property by address, parcel number, owner name, or GPS coordinates and pull parcel-level intelligence like owner details, assessed value, sale history, acreage, zoning, flood-zone clues, and building facts, then pair that with skip-trace style research so they can understand both the land and the person behind it before making a move. |
| [`linear`](./packages/linear) | `@mad-scientist-skills/linear` | Linear: manage issues, projects, teams via GraphQL + curl. |
| [`llama-cpp`](./packages/llama-cpp) | `@mad-scientist-skills/llama-cpp` | llama.cpp local GGUF inference + HF Hub model discovery. |
| [`llm-wiki`](./packages/llm-wiki) | `@mad-scientist-skills/llm-wiki` | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| [`macos-computer-use`](./packages/macos-computer-use) | `@mad-scientist-skills/macos-computer-use` | \| |
| [`mad-census-baby`](./packages/mad-census-baby) | `@mad-scientist-skills/mad-census-baby` | Fetches demographic and census data from the US Census Bureau API based on user-provided location information (city, state, zip code, or address). Outputs data in markdown, CSV, or basic PDF format. Use this skill when you need to retrieve population, housing, or economic data for a specific geographic area. |
| [`mad-event-maker`](./packages/mad-event-maker) | `@mad-scientist-skills/mad-event-maker` | Generate high-converting event copy for The Real Deal Meetup in Charles Blair's voice. Use when the user wants to create, draft, write, or craft event posts, meetup announcements, or marketing copy for Real Deal Meetup events. Triggers on phrases like "create an event post", "write event copy", "draft a meetup announcement", "make an event", "event for Real Deal Meetup", or when the user provides event details (date, time, location, title, topic). |
| [`mad-graphic-designer-skill`](./packages/mad-graphic-designer-skill) | `@mad-scientist-skills/mad-graphic-designer-skill` | mad-graphic-designer-skill lets the user create branded visual assets such as infographics, social graphics, promotional images, event visuals, and marketing design pieces with a stronger strategic and aesthetic point of view, so ideas can be turned into graphics that feel intentional, on-brand, and built to communicate something clearly. |
| [`mad-skip-trace`](./packages/mad-skip-trace) | `@mad-scientist-skills/mad-skip-trace` | mad-skip-trace lets the user dig up likely owner or contact information for a person or property lead by combining identity clues, address data, and public web signals into a practical outreach profile, making it useful for finding who owns a deal, how to reach them, and what supporting details help confirm the match before calling, texting, or mailing. |
| [`manim-video`](./packages/manim-video) | `@mad-scientist-skills/manim-video` | Manim CE animations: 3Blue1Brown math/algo videos. |
| [`maps`](./packages/maps) | `@mad-scientist-skills/maps` | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| [`mcporter`](./packages/mcporter) | `@mad-scientist-skills/mcporter` | Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. |
| [`mcporter-agent`](./packages/mcporter-agent) | `@mad-scientist-skills/mcporter-agent` | Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. |
| [`melissa-data-information`](./packages/melissa-data-information) | `@mad-scientist-skills/melissa-data-information` | melissa-data-information lets the user look up a single property address or process a CSV of multiple addresses to enrich them with Melissa Data property and ownership information, which is useful when they want to verify addresses, get property characteristics, or add structured property data to leads without manual research. |
| [`minecraft-modpack-server`](./packages/minecraft-modpack-server) | `@mad-scientist-skills/minecraft-modpack-server` | Host modded Minecraft servers (CurseForge, Modrinth). |
| [`ml-paper-writing`](./packages/ml-paper-writing) | `@mad-scientist-skills/ml-paper-writing` | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, verifying citations, or preparing camera-ready submissions. Includes LaTeX templates, reviewer guidelines, and citation verification workflows. |
| [`modal-serverless-gpu`](./packages/modal-serverless-gpu) | `@mad-scientist-skills/modal-serverless-gpu` | Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as APIs, or running batch jobs with automatic scaling. |
| [`nano-banana-image-gen`](./packages/nano-banana-image-gen) | `@mad-scientist-skills/nano-banana-image-gen` | Generate images using Gemini 3.1 Flash (gemini-3.1-flash-image-preview) — the nano-banana model. Use for thumbnails, infographics, social graphics, and any image generation task. Always use this instead of the image_generate tool (FLUX). Supports reference image input for face/style matching. |
| [`nano-banana-pro`](./packages/nano-banana-pro) | `@mad-scientist-skills/nano-banana-pro` | Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image. |
| [`nano-pdf`](./packages/nano-pdf) | `@mad-scientist-skills/nano-pdf` | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). |
| [`native-mcp`](./packages/native-mcp) | `@mad-scientist-skills/native-mcp` | MCP client: connect servers, register tools (stdio/HTTP). |
| [`node-connect`](./packages/node-connect) | `@mad-scientist-skills/node-connect` | Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl. |
| [`node-inspect-debugger`](./packages/node-inspect-debugger) | `@mad-scientist-skills/node-inspect-debugger` | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| [`notion`](./packages/notion) | `@mad-scientist-skills/notion` | Notion API via curl: pages, databases, blocks, search. |
| [`notion-beautiful-systems`](./packages/notion-beautiful-systems) | `@mad-scientist-skills/notion-beautiful-systems` | notion-beautiful-systems lets the user create, redesign, migrate, publish, and maintain beautiful Notion workspaces and pages, which is useful when they want a polished knowledge base, a clean team wiki, a well-organized CRM, or any Notion setup that looks professional and works effortlessly without needing to figure out Notion's design patterns themselves. |
| [`notion-cli`](./packages/notion-cli) | `@mad-scientist-skills/notion-cli` | notion-cli lets the user create, read, update, and manage pages, databases, comments, files, and Workers in Notion through the command line, which is useful when they want to save AI outputs, build internal knowledge bases, create structured documents, or automate Notion workflows without clicking through the UI. |
| [`notion-mastery`](./packages/notion-mastery) | `@mad-scientist-skills/notion-mastery` | Build beautiful, well-organized Notion pages and databases — from a single meeting note to a full team wiki, CRM, OKR tracker, or project hub. Use this skill whenever the user mentions Notion, asks to create or update a Notion page or database, wants to design a workspace, build a template, sync content into Notion, or even hints at workflows like "wiki", "team space", "project tracker", "second brain", "meeting notes hub", "PARA", "Zettelkasten", "company knowledge base", or "personal dashboard" — even if they don't explicitly say "Notion". Also triggers on Notion API questions, block JSON, database schema design, property types, formula syntax, relations, rollups, and on requests to convert markdown or other documents into Notion. Designed to work in agents that consume the agentskills.io SKILL.md format (Anthropic, Hermes Agent, OpenClaw) whether they call the API via MCP, the official SDK, or raw HTTP. |
| [`nova-youtube-agent`](./packages/nova-youtube-agent) | `@mad-scientist-skills/nova-youtube-agent` | nova-youtube-agent lets the user run YouTube-focused research and production tasks such as analyzing channel content, extracting insights from videos, helping shape video ideas, and supporting YouTube growth workflows, so they can move from raw video data or channel questions to usable strategy, summaries, and next-step content decisions faster. |
| [`obliteratus`](./packages/obliteratus) | `@mad-scientist-skills/obliteratus` | OBLITERATUS: abliterate LLM refusals (diff-in-means). |
| [`obsidian`](./packages/obsidian) | `@mad-scientist-skills/obsidian` | Read, search, create, and edit notes in the Obsidian vault. |
| [`ocr-and-documents`](./packages/ocr-and-documents) | `@mad-scientist-skills/ocr-and-documents` | Extract text from PDFs/scans (pymupdf, marker-pdf). |
| [`openai-whisper-api`](./packages/openai-whisper-api) | `@mad-scientist-skills/openai-whisper-api` | Transcribe audio via OpenAI Audio Transcriptions API (Whisper). |
| [`openclaw-access-troubleshooting`](./packages/openclaw-access-troubleshooting) | `@mad-scientist-skills/openclaw-access-troubleshooting` | How to find, access, and interact with OpenClaw when the CLI binary isn't in PATH. Covers gateway API, config paths, ports, and alternative interaction methods. |
| [`openclaw-agent-browser`](./packages/openclaw-agent-browser) | `@mad-scientist-skills/openclaw-agent-browser` | Headless browser automation CLI for AI agents. Use when interacting with websites — navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, scraping, testing web apps, downloading files, or automating any browser task. Triggers on requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data", "test this web app", "login to a site", "monitor a page", or any task requiring programmatic web interaction. |
| [`openclaw-agent-creation`](./packages/openclaw-agent-creation) | `@mad-scientist-skills/openclaw-agent-creation` | Create a new OpenClaw subagent workspace with full file structure, modeled after existing agents. Use this when the user wants to add a new named AI agent to their team. |
| [`openclaw-docker-migration`](./packages/openclaw-docker-migration) | `@mad-scientist-skills/openclaw-docker-migration` | Migrate OpenClaw to Hermes when OpenClaw runs inside Docker (no host ~/.openclaw). Covers data extraction from Docker, running the migration script, verifying coexistence, and porting custom skills. Use when a VPS has OpenClaw containerized and the user wants Hermes alongside or instead. |
| [`openclaw-logo-maker`](./packages/openclaw-logo-maker) | `@mad-scientist-skills/openclaw-logo-maker` | openclaw-logo-maker lets the user design and generate logos and brand identity visuals for OpenClaw sub-agents, helping them create consistent, recognizable branding across an AI agent team without needing a graphic designer. |
| [`openclaw-platform-management`](./packages/openclaw-platform-management) | `@mad-scientist-skills/openclaw-platform-management` | OpenClaw platform operations — access/troubleshooting, subagent creation, and Docker migration on Charles's Hostinger server. Covers gateway ports, config management, Docker exec patterns, and agent registration. |
| [`opencode`](./packages/opencode) | `@mad-scientist-skills/opencode` | Delegate coding to OpenCode CLI (features, PR review). |
| [`openhue`](./packages/openhue) | `@mad-scientist-skills/openhue` | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |
| [`opus-blotato-video-poster`](./packages/opus-blotato-video-poster) | `@mad-scientist-skills/opus-blotato-video-poster` | opus-blotato-video-poster lets the user take video clips and push them through a posting workflow that connects clipping and distribution, so they can go from finished short-form video to published social content with less manual handling, especially when they want a more repeatable system for sending videos across multiple channels. |
| [`opus-clip-mcp`](./packages/opus-clip-mcp) | `@mad-scientist-skills/opus-clip-mcp` | opus-clip-mcp lets the user create short-form video clips from longer video content using an Opus-style clipping workflow, helping them identify strong moments, cut usable segments, and prepare social-ready clips that are better suited for platforms like TikTok, Instagram Reels, and YouTube Shorts than the original long-form format. |
| [`outlines`](./packages/outlines) | `@mad-scientist-skills/outlines` | Outlines: structured JSON/regex/Pydantic LLM generation. |
| [`owner-skip-trace`](./packages/owner-skip-trace) | `@mad-scientist-skills/owner-skip-trace` | owner-skip-trace lets the user start from a property or owner name and identify the most likely current owner contact details, including phones, emails, mailing addresses, and related people or entity clues, so they can go from raw property lead to direct-owner outreach with less guesswork and fewer dead ends. |
| [`p5js`](./packages/p5js) | `@mad-scientist-skills/p5js` | p5.js sketches: gen art, shaders, interactive, 3D. |
| [`pdf-generation`](./packages/pdf-generation) | `@mad-scientist-skills/pdf-generation` | pdf-generation lets the user create PDF documents from text, HTML, or structured data when weasyprint fails due to font subsetting bugs, using fpdf2 as a reliable fallback so they can still produce clean, usable PDFs for reports, invoices, or printed materials. |
| [`peft-fine-tuning`](./packages/peft-fine-tuning) | `@mad-scientist-skills/peft-fine-tuning` | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem. |
| [`pikastream-video-meeting`](./packages/pikastream-video-meeting) | `@mad-scientist-skills/pikastream-video-meeting` | pikastream-video-meeting lets the user join a Google Meet or Zoom call as an AI video meeting agent via PikaStreaming, which is useful when they need a virtual agent to attend a meeting, take notes, observe, or participate on their behalf without being physically present. |
| [`pixel-art`](./packages/pixel-art) | `@mad-scientist-skills/pixel-art` | Pixel art w/ era palettes (NES, Game Boy, PICO-8). |
| [`plan`](./packages/plan) | `@mad-scientist-skills/plan` | Plan mode: write markdown plan to .hermes/plans/, no exec. |
| [`pokemon-player`](./packages/pokemon-player) | `@mad-scientist-skills/pokemon-player` | Play Pokemon via headless emulator + RAM reads. |
| [`polymarket`](./packages/polymarket) | `@mad-scientist-skills/polymarket` | Query Polymarket: markets, prices, orderbooks, history. |
| [`popular-web-designs`](./packages/popular-web-designs) | `@mad-scientist-skills/popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| [`powerpoint`](./packages/powerpoint) | `@mad-scientist-skills/powerpoint` | Create, read, edit .pptx decks, slides, notes, templates. |
| [`pretext`](./packages/pretext) | `@mad-scientist-skills/pretext` | Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kinetic typography, and text-powered generative art. Produces single-file HTML demos by default. |
| [`property-contact-research`](./packages/property-contact-research) | `@mad-scientist-skills/property-contact-research` | property-contact-research lets the user look up property owners, parcels, and contact information using paid APIs like BatchData, LandGlide, Rentcast, and free public web sources, covering the full workflow from an address to the owner's name, phone, email, and social signals so they can move from raw lead to direct outreach without switching between tools. |
| [`python-debugpy`](./packages/python-debugpy) | `@mad-scientist-skills/python-debugpy` | Debug Python: pdb REPL + debugpy remote (DAP). |
| [`pytorch-fsdp`](./packages/pytorch-fsdp) | `@mad-scientist-skills/pytorch-fsdp` | Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2 |
| [`reels-text-overlay`](./packages/reels-text-overlay) | `@mad-scientist-skills/reels-text-overlay` | Add AI voiceover and viral-style text overlays to short-form video clips (Reels, Shorts, TikTok). Use after generating or receiving a raw video clip when Charles wants to add narration and/or captions before posting. Covers OpenAI TTS voiceover generation, ffmpeg audio merge, and ffmpeg drawtext overlays in the viral Reels format (big bold white text, black stroke, timed reveals, orange brand accents). |
| [`rei-ai-weekly-newsletter`](./packages/rei-ai-weekly-newsletter) | `@mad-scientist-skills/rei-ai-weekly-newsletter` | rei-ai-weekly-newsletter lets the user generate and deliver a weekly AI-powered newsletter for real estate investors, automatically pulling content from news sites, AI directories, REI blogs, YouTube, Reddit, and Twitter/X, then packaging it into a branded PDF and delivering it via Telegram so subscribers stay informed without spending hours researching manually. |
| [`rei-ai-zoom-processor`](./packages/rei-ai-zoom-processor) | `@mad-scientist-skills/rei-ai-zoom-processor` | rei-ai-zoom-processor lets the user turn a Zoom or any video transcript into a structured Markdown document and PDF with bullet-point summaries, timestamps, and extracted resources, which is useful when they want to capture meeting notes, create training materials, or turn recorded conversations into searchable, shareable documents without manual summarization. |
| [`remotion`](./packages/remotion) | `@mad-scientist-skills/remotion` | Programmatic video creation using React. Use this skill when you need to create, edit, or render videos using code, leverage Remotion's React-based framework for animations, or manage data-driven video production. Triggers on "Remotion", "programmatic video", "render video with react", or requests to create videos via code. |
| [`remotion-video-editing`](./packages/remotion-video-editing) | `@mad-scientist-skills/remotion-video-editing` | Create, edit, and render videos using Remotion — a React-based video-as-code framework. Covers setup from scratch, project structure, key commands, core concepts, and known pitfalls. |
| [`rentcast-property-report`](./packages/rentcast-property-report) | `@mad-scientist-skills/rentcast-property-report` | rentcast-property-report lets the user generate a structured property report with useful real estate data such as ownership information, property characteristics, valuation signals, rent estimates, comps-related context, and market-facing details, giving them a sharper picture of a property's numbers and story before underwriting, marketing, or contacting the owner. |
| [`requesting-code-review`](./packages/requesting-code-review) | `@mad-scientist-skills/requesting-code-review` | Pre-commit review: security scan, quality gates, auto-fix. |
| [`research-paper-writing`](./packages/research-paper-writing) | `@mad-scientist-skills/research-paper-writing` | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |
| [`sarah-outbound-caller`](./packages/sarah-outbound-caller) | `@mad-scientist-skills/sarah-outbound-caller` | sarah-outbound-caller lets the user deploy and manage Sarah, a VAPI-powered AI voice assistant that runs four distinct outbound call types — REI property acquisition, event reminders, community engagement, and agency outreach — with strict script isolation per campaign, which is useful when they want to automate calling campaigns, set up new call flows, or manage multi-vertical outreach without manual dialing. |
| [`seedance-2-video-maker`](./packages/seedance-2-video-maker) | `@mad-scientist-skills/seedance-2-video-maker` | Generate videos using Seedance 2.0 via KIE.AI API - text-to-video, image-to-video, and multimodal reference-to-video with camera controls and audio generation |
| [`segment-anything-model`](./packages/segment-anything-model) | `@mad-scientist-skills/segment-anything-model` | SAM: zero-shot image segmentation via points, boxes, masks. |
| [`seo-audit`](./packages/seo-audit) | `@mad-scientist-skills/seo-audit` | seo-audit lets the user audit, review, and diagnose SEO issues on their website by checking on-page elements, meta tags, technical health, and ranking factors, which is useful when they want to understand why they are not ranking, identify quick wins, or get a structured health check before pursuing a broader SEO strategy. |
| [`service-deployment-and-monitoring`](./packages/service-deployment-and-monitoring) | `@mad-scientist-skills/service-deployment-and-monitoring` | Service deployment, auto-healing monitoring, and port management for Charles's Hostinger server. Covers Traefik Docker routing, systemd port reservation, Docker-in-Docker patterns, health checks, and alerting. |
| [`service-health-monitoring`](./packages/service-health-monitoring) | `@mad-scientist-skills/service-health-monitoring` | service-health-monitoring lets the user keep services running automatically by setting up cron jobs that watch for failures and send Telegram alerts, with auto-healing actions like restarting containers or processes so nothing stays down unattended even when no one is watching. |
| [`serving-llms-vllm`](./packages/serving-llms-vllm) | `@mad-scientist-skills/serving-llms-vllm` | vLLM: high-throughput LLM serving, OpenAI API, quantization. |
| [`sketch`](./packages/sketch) | `@mad-scientist-skills/sketch` | Throwaway HTML mockups: 2-3 design variants to compare. |
| [`skill-to-web-app`](./packages/skill-to-web-app) | `@mad-scientist-skills/skill-to-web-app` | Wrap an existing Hermes skill as a public-facing website deployed on Vercel |
| [`songsee`](./packages/songsee) | `@mad-scientist-skills/songsee` | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| [`songwriting-and-ai-music`](./packages/songwriting-and-ai-music) | `@mad-scientist-skills/songwriting-and-ai-music` | Songwriting craft and Suno AI music prompts. |
| [`spike`](./packages/spike) | `@mad-scientist-skills/spike` | Throwaway experiments to validate an idea before build. |
| [`spotify`](./packages/spotify) | `@mad-scientist-skills/spotify` | Spotify: play, search, queue, manage playlists and devices. |
| [`stable-diffusion-image-generation`](./packages/stable-diffusion-image-generation) | `@mad-scientist-skills/stable-diffusion-image-generation` | State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines. |
| [`subagent-driven-development`](./packages/subagent-driven-development) | `@mad-scientist-skills/subagent-driven-development` | Execute plans via delegate_task subagents (2-stage review). |
| [`supadata-transcript`](./packages/supadata-transcript) | `@mad-scientist-skills/supadata-transcript` | supadata-transcript lets the user pull transcript data from supported media sources so they can read, analyze, quote, summarize, repurpose, or mine spoken content without manually transcribing it, which is especially useful for turning videos, interviews, and recorded conversations into searchable text that can feed content creation or research workflows. |
| [`systematic-debugging`](./packages/systematic-debugging) | `@mad-scientist-skills/systematic-debugging` | 4-phase root cause debugging: understand bugs before fixing. |
| [`systemd-port-reservation`](./packages/systemd-port-reservation) | `@mad-scientist-skills/systemd-port-reservation` | Lock a specific port to a long-running Node/Vite service using systemd — prevents any other process from stealing it, auto-restarts on crash, survives reboots. |
| [`teams-meeting-pipeline`](./packages/teams-meeting-pipeline) | `@mad-scientist-skills/teams-meeting-pipeline` | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions. |
| [`test-driven-development`](./packages/test-driven-development) | `@mad-scientist-skills/test-driven-development` | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| [`touchdesigner-mcp`](./packages/touchdesigner-mcp) | `@mad-scientist-skills/touchdesigner-mcp` | Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools. |
| [`traefik-docker-deploy`](./packages/traefik-docker-deploy) | `@mad-scientist-skills/traefik-docker-deploy` | Deploy Docker apps behind Traefik reverse proxy on Charles's Hostinger server. Handles SSL, DNS, permissions, and firewall. |
| [`unsloth`](./packages/unsloth) | `@mad-scientist-skills/unsloth` | Unsloth: 2-5x faster LoRA/QLoRA fine-tuning, less VRAM. |
| [`veed-fabtoc-1-0`](./packages/veed-fabtoc-1-0) | `@mad-scientist-skills/veed-fabtoc-1-0` | veed_fabtoc_1.0 lets the user create a talking video by combining one user-provided image with text and audio, which is useful when they want to produce a simple AI avatar-style video without complex video editing software or filming. |
| [`vercel`](./packages/vercel) | `@mad-scientist-skills/vercel` | Deploy applications and manage projects with complete CLI reference. Commands for deployments, projects, domains, environment variables, and live documentation access. |
| [`vercel-deploy`](./packages/vercel-deploy) | `@mad-scientist-skills/vercel-deploy` | Deploy a Next.js project to Vercel using the CLI with a stored API token. |
| [`vercel-runner`](./packages/vercel-runner) | `@mad-scientist-skills/vercel-runner` | Manage Vercel from OpenClaw: list projects, get production URLs, list deployments, and redeploy — via the Vercel REST API. |
| [`vercel-site-deploy`](./packages/vercel-site-deploy) | `@mad-scientist-skills/vercel-site-deploy` | Create and deploy websites to Vercel — static HTML workflow that avoids build errors |
| [`video-frames`](./packages/video-frames) | `@mad-scientist-skills/video-frames` | Extract frames or short clips from videos using ffmpeg. |
| [`video-transcribe-and-timestamp`](./packages/video-transcribe-and-timestamp) | `@mad-scientist-skills/video-transcribe-and-timestamp` | video-transcribe-and-timestamp lets the user convert spoken video content into text with timestamps attached to the right moments, which is useful for editing, captioning, quote extraction, clip selection, summaries, training material, and finding exactly where key statements happen inside a longer recording. |
| [`watch`](./packages/watch) | `@mad-scientist-skills/watch` | Watch a video (URL or local path). Downloads with yt-dlp, extracts auto-scaled frames with ffmpeg, pulls the transcript from captions (or Whisper API fallback), and hands the result to Claude so it can answer questions about what's in the video. |
| [`weather`](./packages/weather) | `@mad-scientist-skills/weather` | weather lets the user get current weather conditions and forecasts for any location without needing an API key, which is useful when they want a quick weather check for a property site, a listing area, a travel decision, or any planning that depends on weather conditions. |
| [`weights-and-biases`](./packages/weights-and-biases) | `@mad-scientist-skills/weights-and-biases` | W&B: log ML experiments, sweeps, model registry, dashboards. |
| [`whisper`](./packages/whisper) | `@mad-scientist-skills/whisper` | OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR. |
| [`writing-plans`](./packages/writing-plans) | `@mad-scientist-skills/writing-plans` | Write implementation plans: bite-sized tasks, paths, code. |
| [`xitter`](./packages/xitter) | `@mad-scientist-skills/xitter` | xitter X/Twitter via xurl CLI lets the user create, manage, and publish content on X/Twitter through the xurl command-line workflow, which is useful for posting tweets, threading ideas, testing messaging, automating social distribution, and handling X-related publishing tasks in a more controlled, scriptable way than doing everything manually in the app. |
| [`xurl`](./packages/xurl) | `@mad-scientist-skills/xurl` | X/Twitter via xurl CLI: post, search, DM, media, v2 API. |
| [`youtube-content`](./packages/youtube-content) | `@mad-scientist-skills/youtube-content` | Fetch YouTube video transcripts and transform them into structured content (chapters, summaries, threads, blog posts). |
| [`youtube-opus-skill`](./packages/youtube-opus-skill) | `@mad-scientist-skills/youtube-opus-skill` | youtube-opus-skill lets the user take YouTube content and turn it into high-value short-form opportunities by extracting strong moments, shaping clips, and preparing content for wider distribution, making it useful when they want to squeeze more reach, engagement, and downstream content assets out of a longer YouTube video. |
| [`yt-thumbnail-creator`](./packages/yt-thumbnail-creator) | `@mad-scientist-skills/yt-thumbnail-creator` | yt-thumbnail-creator lets the user create YouTube thumbnails designed to improve click-through rate by combining strong visual hierarchy, readable text, compelling composition, and topic-specific styling, so they can turn a video concept or title into a thumbnail that is built to compete in the feed instead of blending into it. |
| [`yuanbao`](./packages/yuanbao) | `@mad-scientist-skills/yuanbao` | Yuanbao groups: @mention users, query info/members. |

## Quality Notes

- Each package contains exactly one top-level `SKILL.md`.
- Package names use the `@mad-scientist-skills/` scope.
- Live secrets must stay in local `.env` files and out of git.
- Generated cache files such as `__pycache__` and `*.pyc` are ignored.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
