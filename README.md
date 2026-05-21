# Mad Scientist Skill Monorepo

<p align="center">
  <strong>169 standalone Mad Scientist agent skills, flattened into individually installable packages.</strong>
</p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/skills-169-111827?style=for-the-badge">
  <img alt="Packages" src="https://img.shields.io/badge/packages-169-7c3aed?style=for-the-badge">
  <img alt="Workspace" src="https://img.shields.io/badge/workspace-pnpm-2563eb?style=for-the-badge">
  <img alt="Layout" src="https://img.shields.io/badge/layout-flat-059669?style=for-the-badge">
</p>

---

## What This Is

This repository is a flat monorepo of standalone `SKILL.md` packages. Every skill has its own package identity under `packages/<skill-slug>/`; there are no category folders and no category grouping.

Each package preserves the skill's instructions and supporting files such as scripts, references, examples, workflows, tests, templates, and assets.

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

## Quick Start

```bash
git clone https://github.com/Mad-Scientist-sudo/Mad-scientist-skill-monorepo.git
cd Mad-scientist-skill-monorepo
pnpm install
pnpm list
```

Inspect one skill:

```bash
cd packages/weather
sed -n '1,120p' SKILL.md
```

## Package Index

| Skill | Package |
|---|---|
| [`agent-browser`](./packages/agent-browser) | `@mad-scientist-skills/agent-browser` |
| [`agentmail`](./packages/agentmail) | `@mad-scientist-skills/agentmail` |
| [`agentmail-productivity`](./packages/agentmail-productivity) | `@mad-scientist-skills/agentmail-productivity` |
| [`airtable`](./packages/airtable) | `@mad-scientist-skills/airtable` |
| [`apify`](./packages/apify) | `@mad-scientist-skills/apify` |
| [`apple-notes`](./packages/apple-notes) | `@mad-scientist-skills/apple-notes` |
| [`apple-reminders`](./packages/apple-reminders) | `@mad-scientist-skills/apple-reminders` |
| [`architecture-diagram`](./packages/architecture-diagram) | `@mad-scientist-skills/architecture-diagram` |
| [`arxiv`](./packages/arxiv) | `@mad-scientist-skills/arxiv` |
| [`ascii-art`](./packages/ascii-art) | `@mad-scientist-skills/ascii-art` |
| [`ascii-video`](./packages/ascii-video) | `@mad-scientist-skills/ascii-video` |
| [`audiocraft-audio-generation`](./packages/audiocraft-audio-generation) | `@mad-scientist-skills/audiocraft-audio-generation` |
| [`axolotl`](./packages/axolotl) | `@mad-scientist-skills/axolotl` |
| [`baoyu-comic`](./packages/baoyu-comic) | `@mad-scientist-skills/baoyu-comic` |
| [`baoyu-infographic`](./packages/baoyu-infographic) | `@mad-scientist-skills/baoyu-infographic` |
| [`batchdata-skip-trace`](./packages/batchdata-skip-trace) | `@mad-scientist-skills/batchdata-skip-trace` |
| [`beautiful-websites`](./packages/beautiful-websites) | `@mad-scientist-skills/beautiful-websites` |
| [`blogwatcher`](./packages/blogwatcher) | `@mad-scientist-skills/blogwatcher` |
| [`blotato-text-poster`](./packages/blotato-text-poster) | `@mad-scientist-skills/blotato-text-poster` |
| [`brave-search`](./packages/brave-search) | `@mad-scientist-skills/brave-search` |
| [`browser-use-cloud`](./packages/browser-use-cloud) | `@mad-scientist-skills/browser-use-cloud` |
| [`browser-use-cloud-openclaw`](./packages/browser-use-cloud-openclaw) | `@mad-scientist-skills/browser-use-cloud-openclaw` |
| [`census-data`](./packages/census-data) | `@mad-scientist-skills/census-data` |
| [`claude-code`](./packages/claude-code) | `@mad-scientist-skills/claude-code` |
| [`claude-design`](./packages/claude-design) | `@mad-scientist-skills/claude-design` |
| [`clip`](./packages/clip) | `@mad-scientist-skills/clip` |
| [`code-review`](./packages/code-review) | `@mad-scientist-skills/code-review` |
| [`codebase-inspection`](./packages/codebase-inspection) | `@mad-scientist-skills/codebase-inspection` |
| [`codex`](./packages/codex) | `@mad-scientist-skills/codex` |
| [`comfyui`](./packages/comfyui) | `@mad-scientist-skills/comfyui` |
| [`content-repurposer`](./packages/content-repurposer) | `@mad-scientist-skills/content-repurposer` |
| [`content-repurposing-engine`](./packages/content-repurposing-engine) | `@mad-scientist-skills/content-repurposing-engine` |
| [`copywriting`](./packages/copywriting) | `@mad-scientist-skills/copywriting` |
| [`daily-eod-report`](./packages/daily-eod-report) | `@mad-scientist-skills/daily-eod-report` |
| [`data-infographic-generator`](./packages/data-infographic-generator) | `@mad-scientist-skills/data-infographic-generator` |
| [`debugging-hermes-tui-commands`](./packages/debugging-hermes-tui-commands) | `@mad-scientist-skills/debugging-hermes-tui-commands` |
| [`design-md`](./packages/design-md) | `@mad-scientist-skills/design-md` |
| [`discord`](./packages/discord) | `@mad-scientist-skills/discord` |
| [`docker-management`](./packages/docker-management) | `@mad-scientist-skills/docker-management` |
| [`dspy`](./packages/dspy) | `@mad-scientist-skills/dspy` |
| [`evaluating-llms-harness`](./packages/evaluating-llms-harness) | `@mad-scientist-skills/evaluating-llms-harness` |
| [`excalidraw`](./packages/excalidraw) | `@mad-scientist-skills/excalidraw` |
| [`fal-ai-video-generation`](./packages/fal-ai-video-generation) | `@mad-scientist-skills/fal-ai-video-generation` |
| [`find-nearby`](./packages/find-nearby) | `@mad-scientist-skills/find-nearby` |
| [`findmy`](./packages/findmy) | `@mad-scientist-skills/findmy` |
| [`fine-tuning-with-trl`](./packages/fine-tuning-with-trl) | `@mad-scientist-skills/fine-tuning-with-trl` |
| [`firecrawl`](./packages/firecrawl) | `@mad-scientist-skills/firecrawl` |
| [`firehose`](./packages/firehose) | `@mad-scientist-skills/firehose` |
| [`fish-audio-tts`](./packages/fish-audio-tts) | `@mad-scientist-skills/fish-audio-tts` |
| [`frontend-design`](./packages/frontend-design) | `@mad-scientist-skills/frontend-design` |
| [`gemini-image-editor`](./packages/gemini-image-editor) | `@mad-scientist-skills/gemini-image-editor` |
| [`gguf-quantization`](./packages/gguf-quantization) | `@mad-scientist-skills/gguf-quantization` |
| [`github-auth`](./packages/github-auth) | `@mad-scientist-skills/github-auth` |
| [`github-code-review`](./packages/github-code-review) | `@mad-scientist-skills/github-code-review` |
| [`github-issues`](./packages/github-issues) | `@mad-scientist-skills/github-issues` |
| [`github-pr-workflow`](./packages/github-pr-workflow) | `@mad-scientist-skills/github-pr-workflow` |
| [`github-repo-management`](./packages/github-repo-management) | `@mad-scientist-skills/github-repo-management` |
| [`godmode`](./packages/godmode) | `@mad-scientist-skills/godmode` |
| [`gohighlevel-api`](./packages/gohighlevel-api) | `@mad-scientist-skills/gohighlevel-api` |
| [`google-workspace`](./packages/google-workspace) | `@mad-scientist-skills/google-workspace` |
| [`gpt-image-2`](./packages/gpt-image-2) | `@mad-scientist-skills/gpt-image-2` |
| [`graphic-design`](./packages/graphic-design) | `@mad-scientist-skills/graphic-design` |
| [`grpo-rl-training`](./packages/grpo-rl-training) | `@mad-scientist-skills/grpo-rl-training` |
| [`guidance`](./packages/guidance) | `@mad-scientist-skills/guidance` |
| [`hermes-agent`](./packages/hermes-agent) | `@mad-scientist-skills/hermes-agent` |
| [`hermes-agent-setup`](./packages/hermes-agent-setup) | `@mad-scientist-skills/hermes-agent-setup` |
| [`hermes-agent-skill-authoring`](./packages/hermes-agent-skill-authoring) | `@mad-scientist-skills/hermes-agent-skill-authoring` |
| [`hermes-multi-agent-telegram`](./packages/hermes-multi-agent-telegram) | `@mad-scientist-skills/hermes-multi-agent-telegram` |
| [`hermes-workspace-setup`](./packages/hermes-workspace-setup) | `@mad-scientist-skills/hermes-workspace-setup` |
| [`heygen-avatar-video`](./packages/heygen-avatar-video) | `@mad-scientist-skills/heygen-avatar-video` |
| [`himalaya`](./packages/himalaya) | `@mad-scientist-skills/himalaya` |
| [`homedepot-repair-estimator`](./packages/homedepot-repair-estimator) | `@mad-scientist-skills/homedepot-repair-estimator` |
| [`hr-hiring`](./packages/hr-hiring) | `@mad-scientist-skills/hr-hiring` |
| [`huggingface-hub`](./packages/huggingface-hub) | `@mad-scientist-skills/huggingface-hub` |
| [`humanizer`](./packages/humanizer) | `@mad-scientist-skills/humanizer` |
| [`ideation`](./packages/ideation) | `@mad-scientist-skills/ideation` |
| [`image-editing`](./packages/image-editing) | `@mad-scientist-skills/image-editing` |
| [`imessage`](./packages/imessage) | `@mad-scientist-skills/imessage` |
| [`instagram-carousel-authority`](./packages/instagram-carousel-authority) | `@mad-scientist-skills/instagram-carousel-authority` |
| [`jupyter-live-kernel`](./packages/jupyter-live-kernel) | `@mad-scientist-skills/jupyter-live-kernel` |
| [`kanban-orchestrator`](./packages/kanban-orchestrator) | `@mad-scientist-skills/kanban-orchestrator` |
| [`kanban-worker`](./packages/kanban-worker) | `@mad-scientist-skills/kanban-worker` |
| [`landglide-lookup`](./packages/landglide-lookup) | `@mad-scientist-skills/landglide-lookup` |
| [`linear`](./packages/linear) | `@mad-scientist-skills/linear` |
| [`llama-cpp`](./packages/llama-cpp) | `@mad-scientist-skills/llama-cpp` |
| [`llm-wiki`](./packages/llm-wiki) | `@mad-scientist-skills/llm-wiki` |
| [`macos-computer-use`](./packages/macos-computer-use) | `@mad-scientist-skills/macos-computer-use` |
| [`mad-census-baby`](./packages/mad-census-baby) | `@mad-scientist-skills/mad-census-baby` |
| [`mad-event-maker`](./packages/mad-event-maker) | `@mad-scientist-skills/mad-event-maker` |
| [`mad-graphic-designer-skill`](./packages/mad-graphic-designer-skill) | `@mad-scientist-skills/mad-graphic-designer-skill` |
| [`mad-skip-trace`](./packages/mad-skip-trace) | `@mad-scientist-skills/mad-skip-trace` |
| [`manim-video`](./packages/manim-video) | `@mad-scientist-skills/manim-video` |
| [`maps`](./packages/maps) | `@mad-scientist-skills/maps` |
| [`mcporter-agent`](./packages/mcporter-agent) | `@mad-scientist-skills/mcporter-agent` |
| [`melissa-data-information`](./packages/melissa-data-information) | `@mad-scientist-skills/melissa-data-information` |
| [`minecraft-modpack-server`](./packages/minecraft-modpack-server) | `@mad-scientist-skills/minecraft-modpack-server` |
| [`ml-paper-writing`](./packages/ml-paper-writing) | `@mad-scientist-skills/ml-paper-writing` |
| [`modal-serverless-gpu`](./packages/modal-serverless-gpu) | `@mad-scientist-skills/modal-serverless-gpu` |
| [`nano-banana-image-gen`](./packages/nano-banana-image-gen) | `@mad-scientist-skills/nano-banana-image-gen` |
| [`nano-banana-pro`](./packages/nano-banana-pro) | `@mad-scientist-skills/nano-banana-pro` |
| [`nano-pdf`](./packages/nano-pdf) | `@mad-scientist-skills/nano-pdf` |
| [`native-mcp`](./packages/native-mcp) | `@mad-scientist-skills/native-mcp` |
| [`node-inspect-debugger`](./packages/node-inspect-debugger) | `@mad-scientist-skills/node-inspect-debugger` |
| [`notion`](./packages/notion) | `@mad-scientist-skills/notion` |
| [`notion-mastery`](./packages/notion-mastery) | `@mad-scientist-skills/notion-mastery` |
| [`nova-youtube-agent`](./packages/nova-youtube-agent) | `@mad-scientist-skills/nova-youtube-agent` |
| [`obliteratus`](./packages/obliteratus) | `@mad-scientist-skills/obliteratus` |
| [`obsidian`](./packages/obsidian) | `@mad-scientist-skills/obsidian` |
| [`ocr-and-documents`](./packages/ocr-and-documents) | `@mad-scientist-skills/ocr-and-documents` |
| [`openai-whisper-api`](./packages/openai-whisper-api) | `@mad-scientist-skills/openai-whisper-api` |
| [`openclaw-platform-management`](./packages/openclaw-platform-management) | `@mad-scientist-skills/openclaw-platform-management` |
| [`opencode`](./packages/opencode) | `@mad-scientist-skills/opencode` |
| [`openhue`](./packages/openhue) | `@mad-scientist-skills/openhue` |
| [`opus-blotato-video-poster`](./packages/opus-blotato-video-poster) | `@mad-scientist-skills/opus-blotato-video-poster` |
| [`opus-clip-mcp`](./packages/opus-clip-mcp) | `@mad-scientist-skills/opus-clip-mcp` |
| [`outlines`](./packages/outlines) | `@mad-scientist-skills/outlines` |
| [`owner-skip-trace`](./packages/owner-skip-trace) | `@mad-scientist-skills/owner-skip-trace` |
| [`p5js`](./packages/p5js) | `@mad-scientist-skills/p5js` |
| [`pdf-generation`](./packages/pdf-generation) | `@mad-scientist-skills/pdf-generation` |
| [`peft-fine-tuning`](./packages/peft-fine-tuning) | `@mad-scientist-skills/peft-fine-tuning` |
| [`pixel-art`](./packages/pixel-art) | `@mad-scientist-skills/pixel-art` |
| [`plan`](./packages/plan) | `@mad-scientist-skills/plan` |
| [`pokemon-player`](./packages/pokemon-player) | `@mad-scientist-skills/pokemon-player` |
| [`polymarket`](./packages/polymarket) | `@mad-scientist-skills/polymarket` |
| [`popular-web-designs`](./packages/popular-web-designs) | `@mad-scientist-skills/popular-web-designs` |
| [`powerpoint`](./packages/powerpoint) | `@mad-scientist-skills/powerpoint` |
| [`pretext`](./packages/pretext) | `@mad-scientist-skills/pretext` |
| [`property-contact-research`](./packages/property-contact-research) | `@mad-scientist-skills/property-contact-research` |
| [`python-debugpy`](./packages/python-debugpy) | `@mad-scientist-skills/python-debugpy` |
| [`pytorch-fsdp`](./packages/pytorch-fsdp) | `@mad-scientist-skills/pytorch-fsdp` |
| [`reels-text-overlay`](./packages/reels-text-overlay) | `@mad-scientist-skills/reels-text-overlay` |
| [`rei-ai-weekly-newsletter`](./packages/rei-ai-weekly-newsletter) | `@mad-scientist-skills/rei-ai-weekly-newsletter` |
| [`rei-ai-zoom-processor`](./packages/rei-ai-zoom-processor) | `@mad-scientist-skills/rei-ai-zoom-processor` |
| [`remotion`](./packages/remotion) | `@mad-scientist-skills/remotion` |
| [`remotion-video-editing`](./packages/remotion-video-editing) | `@mad-scientist-skills/remotion-video-editing` |
| [`rentcast-property-report`](./packages/rentcast-property-report) | `@mad-scientist-skills/rentcast-property-report` |
| [`requesting-code-review`](./packages/requesting-code-review) | `@mad-scientist-skills/requesting-code-review` |
| [`research-paper-writing`](./packages/research-paper-writing) | `@mad-scientist-skills/research-paper-writing` |
| [`sarah-outbound-caller`](./packages/sarah-outbound-caller) | `@mad-scientist-skills/sarah-outbound-caller` |
| [`seedance-2-video-maker`](./packages/seedance-2-video-maker) | `@mad-scientist-skills/seedance-2-video-maker` |
| [`segment-anything-model`](./packages/segment-anything-model) | `@mad-scientist-skills/segment-anything-model` |
| [`seo-audit`](./packages/seo-audit) | `@mad-scientist-skills/seo-audit` |
| [`service-deployment-and-monitoring`](./packages/service-deployment-and-monitoring) | `@mad-scientist-skills/service-deployment-and-monitoring` |
| [`serving-llms-vllm`](./packages/serving-llms-vllm) | `@mad-scientist-skills/serving-llms-vllm` |
| [`sketch`](./packages/sketch) | `@mad-scientist-skills/sketch` |
| [`songwriting-and-ai-music`](./packages/songwriting-and-ai-music) | `@mad-scientist-skills/songwriting-and-ai-music` |
| [`spike`](./packages/spike) | `@mad-scientist-skills/spike` |
| [`stable-diffusion-image-generation`](./packages/stable-diffusion-image-generation) | `@mad-scientist-skills/stable-diffusion-image-generation` |
| [`subagent-driven-development`](./packages/subagent-driven-development) | `@mad-scientist-skills/subagent-driven-development` |
| [`supadata-transcript`](./packages/supadata-transcript) | `@mad-scientist-skills/supadata-transcript` |
| [`systematic-debugging`](./packages/systematic-debugging) | `@mad-scientist-skills/systematic-debugging` |
| [`teams-meeting-pipeline`](./packages/teams-meeting-pipeline) | `@mad-scientist-skills/teams-meeting-pipeline` |
| [`test-driven-development`](./packages/test-driven-development) | `@mad-scientist-skills/test-driven-development` |
| [`touchdesigner-mcp`](./packages/touchdesigner-mcp) | `@mad-scientist-skills/touchdesigner-mcp` |
| [`unsloth`](./packages/unsloth) | `@mad-scientist-skills/unsloth` |
| [`vercel`](./packages/vercel) | `@mad-scientist-skills/vercel` |
| [`vercel-deploy`](./packages/vercel-deploy) | `@mad-scientist-skills/vercel-deploy` |
| [`vercel-site-deploy`](./packages/vercel-site-deploy) | `@mad-scientist-skills/vercel-site-deploy` |
| [`video-transcribe-and-timestamp`](./packages/video-transcribe-and-timestamp) | `@mad-scientist-skills/video-transcribe-and-timestamp` |
| [`watch`](./packages/watch) | `@mad-scientist-skills/watch` |
| [`weather`](./packages/weather) | `@mad-scientist-skills/weather` |
| [`weights-and-biases`](./packages/weights-and-biases) | `@mad-scientist-skills/weights-and-biases` |
| [`whisper`](./packages/whisper) | `@mad-scientist-skills/whisper` |
| [`writing-plans`](./packages/writing-plans) | `@mad-scientist-skills/writing-plans` |
| [`xitter`](./packages/xitter) | `@mad-scientist-skills/xitter` |
| [`xurl`](./packages/xurl) | `@mad-scientist-skills/xurl` |
| [`youtube-content`](./packages/youtube-content) | `@mad-scientist-skills/youtube-content` |
| [`youtube-opus-skill`](./packages/youtube-opus-skill) | `@mad-scientist-skills/youtube-opus-skill` |
| [`yt-thumbnail-creator`](./packages/yt-thumbnail-creator) | `@mad-scientist-skills/yt-thumbnail-creator` |

## Quality Notes

- Each package contains exactly one top-level `SKILL.md`.
- Package names use the `@mad-scientist-skills/` scope.
- Live secrets must stay in local `.env` files and out of git.
- Generated cache files such as `__pycache__` and `*.pyc` are ignored.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
