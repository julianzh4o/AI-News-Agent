# AI News Agent

> A CLI tool that aggregates global AI news from multiple sources and generates a structured daily digest via your preferred LLM.

---

<center>English | [中文](README-ZH.md)</center>

---

## Table of Contents

- [Features](#features)
- [Quickstart](#quickstart)
- [Installation](#installation)
- [Configuration](#configuration)
- [Data Sources](#data-sources)
- [AI Providers](#ai-providers)
- [Output Format](#output-format)
- [Saving Reports](#saving-reports)
- [FAQ](#faq)
- [Project Structure](#project-structure)
- [License](#license)

---

## Features

- 5 data sources: RSS feeds, ArXiv papers, HackerNews, NewsAPI, Web Search (DuckDuckGo / Tavily / SerpAPI)
- 9 AI providers: Anthropic, OpenAI, Gemini, DeepSeek, Groq, Moonshot, Zhipu, Qwen, Mistral
- Relay/proxy support: set a custom `base_url` per provider for third-party API gateways
- Multilingual output: zh, en, ja, ko, fr, de, es, ru, and more
- Structured digest: auto-categorized by product launches, funding, research breakthroughs, and regulatory news
- Optional Markdown report file saved per run

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/yourname/ai-news-agent.git
cd ai-news-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your config
cp config.example.yaml config.yaml

# 4. Fill in your settings in config.yaml
ai_provider | api_key | base_url | model | language | save_report
# 5. Run
python main.py
```

---

## Installation

### Prerequisites

| Requirement   | Version |
|---------------|---------|
| Python        | >= 3.9  |
| pip           | any     |

### Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies included:

| Package               | Purpose                   |
|-----------------------|---------------------------|
| `anthropic`           | Anthropic Claude API SDK  |
| `openai`              | OpenAI-compat SDK         |
| `feedparser`          | RSS feed parsing          |
| `httpx`               | HTTP requests             |
| `pyyaml`              | Config file parsing       |
| `duckduckgo-search`   | Free web search           |

---

## Configuration

Copy the template and edit `config.yaml`:

```bash
cp config.example.yaml config.yaml
```

### 1. Select AI Provider

```yaml
# Set which provider to use
ai_provider: "anthropic"
```

Options: `anthropic` | `openai` | `gemini` | `deepseek` | `groq` | `moonshot` | `zhipu` | `qwen` | `mistral`

### 2. Fill in API Key

Find your provider under the `providers` block and set `api_key`:

```yaml
providers:
  anthropic:
    api_key: "sk-ant-xxxxxxxxxx"   # Your key here
    base_url: ""                   # Leave empty for official endpoint
    model: "claude-sonnet-4-6"     # Change model if needed
```

### 3. Using an API Relay/Proxy

If you use a third-party API gateway, set `base_url` to the relay URL:

```yaml
providers:
  openai:
    api_key: "your-key"
    base_url: "https://your-relay-domain.com/v1"  # 中转站地址 / Relay URL
    model: "gpt-4o"
```

When `base_url` is empty, the official default endpoint is used automatically.

### 4. Set Output Language

```yaml
# language: "zh" # 中文
# language: "en" # English
# language: "ja" # 日本語
# language: "ko" # 한국어
# language: "fr" # Français
# language: "de" # Deutsch
# language: "es" # Español
# language: "ru" # Русский
```

### 5. Full Configuration Reference

| Field                      | Default            | Description                                  |
|----------------------------|--------------------|----------------------------------------------|
| `ai_provider`              | `"anthropic"`      | Active AI provider                           |
| `language`                 | `"zh"`             | Output language                              |
| `top_n`                    | `10`               | Max articles to display (5–8 selected)       |
| `save_report`              | `false`            | Save Markdown report file                    |
| `report_path`              | `"reports/"`       | Report output directory                      |
| `sources.rss`              | `true`             | Enable RSS feeds                             |
| `sources.arxiv`            | `true`             | Enable ArXiv papers                          |
| `sources.hackernews`       | `true`             | Enable HackerNews                            |
| `sources.newsapi`          | `false`            | Enable NewsAPI (key required)                |
| `sources.websearch`        | `true`             | Enable web search                            |
| `newsapi_key`              | `""`               | NewsAPI key (newsapi.org)                    |
| `arxiv.max_results`        | `20`               | ArXiv fetch limit                            |
| `arxiv.query`              | (AI Keywords)      | ArXiv search query                           |
| `hackernews.min_points`    | `50`               | Minimum HN upvote score                      |
| `hackernews.max_results`   | `15`               | HN fetch limit                               |
| `websearch.engine`         | `"duckduckgo"`     | Search engine                                |
| `websearch.query`          | (AI Keywords)      | Web search query                             |
| `websearch.max_results`    | `10`               | Search result count                          |
| `websearch.tavily_api_key` | `""`               | Tavily key (optional)                        |
| `websearch.serpapi_api_key`| `""`               | SerpAPI key (optional)                       |

---

## Data Sources

### RSS Feeds

The following feeds are built in by default. Edit the `rss_feeds` list in `config.yaml` freely:

| Name                     | Source                    |
|--------------------------|---------------------------|
| OpenAI                   | openai.com                |
| Anthropic                | anthropic.com             |
| Google DeepMind          | deepmind.google           |
| Hugging Face             | huggingface.co            |
| MIT Technology Review AI | technologyreview.com      |
| VentureBeat AI           | venturebeat.com           |
| The Gradient             | thegradient.pub           |

Add a custom RSS feed:

```yaml
rss_feeds:
  - name: "My Custom Feed"
    url: "https://example.com/feed.xml"
```

### ArXiv Papers

Automatically fetches the latest AI-related papers, sorted by submission date descending.

Customize the query:

```yaml
arxiv:
  query: "large language model OR diffusion model"
  max_results: 20
```

### HackerNews

Fetches high-score AI discussions via the Algolia API.

```yaml
hackernews:
  min_points: 50    # 过滤低热度帖子 / Filter low-engagement posts
  max_results: 15
```

### NewsAPI

Requires an API key (free plan available): https://newsapi.org

```yaml
newsapi_key: "your-newsapi-key"
sources:
  newsapi: true
```

### Web Search

Three engines available:

| Engine        | Cost        | Get Key                   |
|---------------|-------------|---------------------------|
| `duckduckgo`  | Free        | Not required              |
| `tavily`      | Paid        | https://tavily.com        |
| `serpapi`     | Paid        | https://serpapi.com       |

Switch engine:

```yaml
websearch:
  engine: "tavily"
  tavily_api_key: "tvly-xxxxxxxxxx"
```

---

## AI Providers

All providers support custom `base_url` (relay gateway) and `model` overrides.

| Provider          | Default Model                 | Key / Get Key                        |
|-------------------|-------------------------------|-------------------------------------------|
| `anthropic`       | claude-sonnet-4-6             | https://console.anthropic.com             |
| `openai`          | gpt-4o                        | https://platform.openai.com               |
| `gemini`          | gemini-2.0-flash              | https://aistudio.google.com               |
| `deepseek`        | deepseek-chat                 | https://platform.deepseek.com             |
| `groq`            | llama-3.3-70b-versatile       | https://console.groq.com                  |
| `moonshot`        | moonshot-v1-8k                | https://platform.moonshot.cn              |
| `zhipu`           | glm-4-flash                   | https://open.bigmodel.cn                  |
| `qwen`            | qwen-plus                     | https://dashscope.aliyun.com              |
| `mistral`         | mistral-large-latest          | https://console.mistral.ai                |

> **Note:** 
> All providers except Anthropic use the OpenAI-compatible API. Switching providers requires
> only changing `ai_provider` and the corresponding `api_key` — no code changes needed.

---

## Output Format

After each run, the terminal outputs a digest in the following format:

```
============================================================
**[Product Launch]** GPT-5 Officially Released: Supports Real-Time Voice and Video Interaction | OpenAI | Summary...

**[Funding & M&A]** AI Safety Company X Raises $200 Million in Series B Funding | TechCrunch | Summary...

**[Tech Breakthrough]** DeepMind Releases AlphaFold 3: Protein Structure Prediction Accuracy Further Improved | ArXiv | Summary...

**[Industry Regulation]** EU AI Act Officially Enters into Force: Mandatory Registration for High-Risk Systems | VentureBeat | Summary...

Today's Trend Commentary: ...
============================================================
```

News is sorted by importance and grouped into four categories (only shown when relevant):

| Category Tag             | Content                          |
|--------------------------|----------------------------------|
| `[Product Launch]`       | Major product launches           |
| `[Funding & M&A]`        | Funding rounds and M&A           |
| `[Tech Breakthrough]`    | Notable papers and breakthroughs |
| `[Industry Regulation]`  | Regulation and governance        |

---

## Saving Reports

When enabled, each run saves the digest as a Markdown file.

```yaml
save_report: true
report_path: "reports/"   # Output directory
```

Generated filename format:

```
reports/ai-news-2026-06-22.md
```

> The `reports/` directory is excluded via `.gitignore` and will not be committed to Git.

---

## FAQ

**Q: I get `config.yaml not found` when running.**

A: Run `cp config.example.yaml config.yaml` to create the config file, then fill in your API key.

---

**Q: I see `providers.anthropic.api_key is not set`.**

A: Open `config.yaml`, find the entry for your current `ai_provider` under `providers`, and set a valid `api_key`.

---

**Q: I'm behind a firewall and can't reach OpenAI / Anthropic directly.**

A: Set `base_url` for the provider to your relay URL, for example:

```yaml
providers:
  openai:
    api_key: "your-key"
    base_url: "https://your-relay.com/v1"
```

---

**Q: How do I use only specific data sources?**

A: Set unwanted sources to `false` in the `sources` block:

```yaml
sources:
  rss: true
  arxiv: false
  hackernews: false
  newsapi: false
  websearch: true
```

---

**Q: How do I switch to a cheaper model (e.g., GPT-4o-mini)?**

A: Change the `model` field under your provider:

```yaml
providers:
  openai:
    api_key: "your-key"
    model: "gpt-4o-mini"
```

---

**Q: Very few articles are being fetched.**

A: Check the following:
- Network access to the sources
- `min_points` too high (try `10`)
- Increase `arxiv.max_results`
- DuckDuckGo may rate-limit; switch to Tavily

---

## Project Structure

```
ai-news-agent/
├── config.example.yaml   # Config template (safe to commit)
├── config.yaml           # Local config with keys (gitignored)
├── requirements.txt      # Python dependencies
├── main.py               # Entry point
├── fetcher.py            # RSS/ArXiv/HN/NewsAPI/WebSearch
├── processor.py          # AI digest generation
├── .gitignore
├── LICENSE
└── reports/              # Generated reports (gitignored)
```

---

[MIT License](LICENSE) © 2026
