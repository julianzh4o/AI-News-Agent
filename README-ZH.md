# AI News Agent

> 一个命令行 AI 资讯聚合工具，自动从多个数据源收集全球 AI 前沿动态，并通过大语言模型生成结构化每日摘要。
>
> A CLI tool that aggregates global AI news from multiple sources and generates a structured daily digest via your preferred LLM.

---

## 目录 / Table of Contents

- [功能特性 / Features](#功能特性--features)
- [快速开始 / Quickstart](#快速开始--quickstart)
- [安装 / Installation](#安装--installation)
- [配置 / Configuration](#配置--configuration)
- [数据源 / Data Sources](#数据源--data-sources)
- [AI 提供商 / AI Providers](#ai-提供商--ai-providers)
- [输出格式 / Output Format](#输出格式--output-format)
- [保存报告 / Saving Reports](#保存报告--saving-reports)
- [常见问题 / FAQ](#常见问题--faq)
- [项目结构 / Project Structure](#项目结构--project-structure)
- [许可证 / License](#许可证--license)

---

## 功能特性 / Features

**中文：**
- 5 大数据源：RSS 订阅、ArXiv 论文、HackerNews、NewsAPI、网络搜索（DuckDuckGo / Tavily / SerpAPI）
- 9 大 AI 提供商：Anthropic、OpenAI、Gemini、DeepSeek、Groq、Moonshot、智谱、通义千问、Mistral
- 支持 API 中转站：每个提供商均可自定义 `base_url`，兼容第三方代理网关
- 多语言输出：中文、英文、日文、韩文、法文、德文、西班牙文、俄文等
- 结构化摘要：按产品发布、融资并购、技术突破、行业规范四类自动归类排序
- 可选保存为 Markdown 日报文件

**English:**
- 5 data sources: RSS feeds, ArXiv papers, HackerNews, NewsAPI, Web Search (DuckDuckGo / Tavily / SerpAPI)
- 9 AI providers: Anthropic, OpenAI, Gemini, DeepSeek, Groq, Moonshot, Zhipu, Qwen, Mistral
- Relay/proxy support: set a custom `base_url` per provider for third-party API gateways
- Multilingual output: zh, en, ja, ko, fr, de, es, ru, and more
- Structured digest: auto-categorized by product launches, funding, research breakthroughs, and regulatory news
- Optional Markdown report file saved per run

---

## 快速开始 / Quickstart

```bash
# 1. 克隆项目
git clone https://github.com/yourname/ai-news-agent.git
cd ai-news-agent

# 2. 安装依赖
pip install -r requirements.txt

# 3. 创建配置文件
cp config.example.yaml config.yaml

# 4. 在 config.yaml 中填入你的设置 
ai_provider | api_key | base_url | model | language | save_report

# 5. 运行
python main.py
```

---

## 安装 / Installation

### 前提条件 / Prerequisites

| 要求 / Requirement | 版本 / Version |
|--------------------|----------------|
| Python             | >= 3.9         |
| pip                | 任意 / any     |

### 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

依赖清单 / Dependencies included:

| 包 / Package          | 用途 / Purpose                        |
|-----------------------|---------------------------------------|
| `anthropic`           | Anthropic Claude API SDK              |
| `openai`              | OpenAI 兼容接口 SDK / OpenAI-compat SDK |
| `feedparser`          | RSS 订阅解析 / RSS feed parsing       |
| `httpx`               | HTTP 请求 / HTTP requests             |
| `pyyaml`              | 配置文件解析 / Config file parsing    |
| `duckduckgo-search`   | 免费网络搜索 / Free web search        |

---

## 配置 / Configuration

复制模板后编辑 `config.yaml`：
Copy the template and edit `config.yaml`:

```bash
cp config.example.yaml config.yaml
```

### 1. 选择 AI 提供商 / Select AI Provider

```yaml
# 设置要使用的提供商名称 / Set which provider to use
ai_provider: "anthropic"
```

可选值 / Options: `anthropic` | `openai` | `gemini` | `deepseek` | `groq` | `moonshot` | `zhipu` | `qwen` | `mistral`

### 2. 填写 API Key / Fill in API Key

在 `providers` 块中找到对应提供商，填入 `api_key`：
Find your provider under the `providers` block and set `api_key`:

```yaml
providers:
  anthropic:
    api_key: "sk-ant-xxxxxxxxxx"   # 填入你的 Key / Your key here
    base_url: ""                   # 留空使用官方地址 / Leave empty for official endpoint
    model: "claude-sonnet-4-6"     # 可修改模型 / Change model if needed
```

### 3. 使用 API 中转站 / Using an API Relay/Proxy

如果你使用第三方 API 代理（中转站），在 `base_url` 填入代理地址：
If you use a third-party API gateway, set `base_url` to the relay URL:

```yaml
providers:
  openai:
    api_key: "your-key"
    base_url: "https://your-relay-domain.com/v1"  # 中转站地址 / Relay URL
    model: "gpt-4o"
```

`base_url` 为空时自动使用官方默认地址。
When `base_url` is empty, the official default endpoint is used automatically.

### 4. 设置输出语言 / Set Output Language

```yaml
language: "zh"   # 中文
# language: "en" # English
# language: "ja" # 日本語
# language: "ko" # 한국어
# language: "fr" # Français
# language: "de" # Deutsch
# language: "es" # Español
# language: "ru" # Русский
```

### 5. 完整配置参考 / Full Configuration Reference

| 字段 / Field              | 默认值 / Default   | 说明 / Description                                          |
|---------------------------|--------------------|-------------------------------------------------------------|
| `ai_provider`             | `"anthropic"`      | 使用的 AI 提供商 / Active AI provider                       |
| `language`                | `"zh"`             | 输出语言 / Output language                                  |
| `top_n`                   | `10`               | 最多展示条数 / Max articles to display (5–8 selected)       |
| `save_report`             | `false`            | 是否保存 Markdown 报告 / Save Markdown report file          |
| `report_path`             | `"reports/"`       | 报告保存目录 / Report output directory                      |
| `sources.rss`             | `true`             | 启用 RSS 订阅 / Enable RSS feeds                            |
| `sources.arxiv`           | `true`             | 启用 ArXiv 论文 / Enable ArXiv papers                      |
| `sources.hackernews`      | `true`             | 启用 HackerNews / Enable HackerNews                         |
| `sources.newsapi`         | `false`            | 启用 NewsAPI（需填 Key）/ Enable NewsAPI (key required)     |
| `sources.websearch`       | `true`             | 启用网络搜索 / Enable web search                            |
| `newsapi_key`             | `""`               | NewsAPI 密钥 / NewsAPI key (newsapi.org)                    |
| `arxiv.max_results`       | `20`               | ArXiv 最多拉取条数 / ArXiv fetch limit                      |
| `arxiv.query`             | (AI 关键词)        | ArXiv 搜索词 / ArXiv search query                           |
| `hackernews.min_points`   | `50`               | HN 最低分数过滤 / Minimum HN upvote score                   |
| `hackernews.max_results`  | `15`               | HN 最多拉取条数 / HN fetch limit                            |
| `websearch.engine`        | `"duckduckgo"`     | 搜索引擎 / Search engine                                    |
| `websearch.query`         | (AI 关键词)        | 搜索关键词 / Web search query                               |
| `websearch.max_results`   | `10`               | 搜索结果数 / Search result count                            |
| `websearch.tavily_api_key`| `""`               | Tavily 密钥（可选）/ Tavily key (optional)                  |
| `websearch.serpapi_api_key`| `""`              | SerpAPI 密钥（可选）/ SerpAPI key (optional)                |

---

## 数据源 / Data Sources

### RSS 订阅 / RSS Feeds

默认内置以下订阅源，可在 `config.yaml` 的 `rss_feeds` 列表中自由增删：
The following feeds are built in by default. Edit the `rss_feeds` list in `config.yaml` freely:

| 名称 / Name              | 来源 / Source             |
|--------------------------|---------------------------|
| OpenAI                   | openai.com                |
| Anthropic                | anthropic.com             |
| Google DeepMind          | deepmind.google           |
| Hugging Face             | huggingface.co            |
| MIT Technology Review AI | technologyreview.com      |
| VentureBeat AI           | venturebeat.com           |
| The Gradient             | thegradient.pub           |

添加自定义 RSS 源 / Add a custom RSS feed:

```yaml
rss_feeds:
  - name: "My Custom Feed"
    url: "https://example.com/feed.xml"
```

### ArXiv 论文 / ArXiv Papers

自动拉取最新 AI 相关论文，按提交日期降序排列。
Automatically fetches the latest AI-related papers, sorted by submission date descending.

修改搜索词 / Customize the query:

```yaml
arxiv:
  query: "large language model OR diffusion model"
  max_results: 20
```

### HackerNews

通过 Algolia API 获取 AI 相关高分讨论帖。
Fetches high-score AI discussions via the Algolia API.

```yaml
hackernews:
  min_points: 50    # 过滤低热度帖子 / Filter low-engagement posts
  max_results: 15
```

### NewsAPI

需要 API Key（免费计划可用）：https://newsapi.org
Requires an API key (free plan available): https://newsapi.org

```yaml
newsapi_key: "your-newsapi-key"
sources:
  newsapi: true
```

### 网络搜索 / Web Search

三种引擎可选 / Three engines available:

| 引擎 / Engine | 费用 / Cost        | 获取 Key / Get Key        |
|---------------|--------------------|---------------------------|
| `duckduckgo`  | 免费 / Free        | 无需 / Not required       |
| `tavily`      | 付费 / Paid        | https://tavily.com        |
| `serpapi`     | 付费 / Paid        | https://serpapi.com       |

切换引擎 / Switch engine:

```yaml
websearch:
  engine: "tavily"
  tavily_api_key: "tvly-xxxxxxxxxx"
```

---

## AI 提供商 / AI Providers

所有提供商均支持自定义 `base_url`（API 中转站）和 `model`（模型名称）。
All providers support custom `base_url` (relay gateway) and `model` overrides.

| 提供商 / Provider | 默认模型 / Default Model       | 获取 Key / Get Key                        |
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

> **提示 / Note:** 除 Anthropic 外，所有提供商均通过 OpenAI 兼容接口调用，切换提供商只需修改
> `ai_provider` 和对应的 `api_key`，无需修改代码。
>
> All providers except Anthropic use the OpenAI-compatible API. Switching providers requires
> only changing `ai_provider` and the corresponding `api_key` — no code changes needed.

---

## 输出格式 / Output Format

每次运行后，终端将输出如下格式的摘要：
After each run, the terminal outputs a digest in the following format:

```
============================================================
**[产品发布]** GPT-5 正式发布，支持实时语音与视频交互 | OpenAI | 摘要内容……

**[融资并购]** AI 安全公司 X 完成 2 亿美元 B 轮融资 | TechCrunch | 摘要内容……

**[技术突破]** DeepMind 发布 AlphaFold 3，蛋白质结构预测精度再提升 | ArXiv | 摘要内容……

**[行业规范]** 欧盟 AI 法案正式生效，高风险系统需强制备案 | VentureBeat | 摘要内容……

今日趋势点评：……
============================================================
```

新闻按重要性排序，分为四类（有相关内容才会出现）：
News is sorted by importance and grouped into four categories (only shown when relevant):

| 分类标签 / Category Tag | 内容 / Content                                       |
|-------------------------|------------------------------------------------------|
| `[产品发布]`            | 主要公司产品更新、新模型发布 / Major product launches |
| `[融资并购]`            | 融资事件、行业并购 / Funding rounds and M&A           |
| `[技术突破]`            | 重要论文、研究成果 / Notable papers and breakthroughs |
| `[行业规范]`            | AI 安全、监管、数据治理动态 / Regulation and governance |

---

## 保存报告

开启后每次运行自动将摘要保存为 Markdown 文件。

```yaml
save_report: true
report_path: "reports/"   # 报告保存目录
```

生成文件名格式:

```
reports/ai-news-2026-06-22.md
```

> **注意:** `reports/` 目录已在 `.gitignore` 中排除，不会被提交到 Git。

---

## 常见问题

**Q: 运行后提示 `config.yaml not found` 怎么办？**

A: 执行 `cp config.example.yaml config.yaml` 创建配置文件，再填入 API Key。

---

**Q: 提示 `providers.anthropic.api_key is not set` 怎么办？**

A: 打开 `config.yaml`，在 `providers` 块中找到当前 `ai_provider` 对应的条目，填入有效的 API Key。

---

**Q: 在中国大陆访问 OpenAI / Anthropic 等接口受限怎么办？**

A: 在对应提供商的 `base_url` 字段填入你的中转站地址，例如：

```yaml
providers:
  openai:
    api_key: "your-key"
    base_url: "https://your-relay.com/v1"
```

---

**Q: 如何只使用部分数据源？**

A: 在 `config.yaml` 的 `sources` 块中将不需要的来源设为 `false`：

```yaml
sources:
  rss: true
  arxiv: false
  hackernews: false
  newsapi: false
  websearch: true
```

---

**Q: 如何更换模型（如使用 GPT-4o-mini 节省费用）？**

A: 修改对应提供商下的 `model` 字段：

```yaml
providers:
  openai:
    api_key: "your-key"
    model: "gpt-4o-mini"
```

---

**Q: 抓取到的文章数量很少，怎么办？**

A: 检查以下几点:
- 网络是否能访问对应数据源
- `hackernews.min_points` 是否设置过高（试试调低到 `10`）
- `arxiv.max_results` 可适当增大
- DuckDuckGo 搜索偶有频率限制，可切换为 Tavily

---

## 项目结构

```
ai-news-agent/
├── config.example.yaml   # 配置模板（可提交）
├── config.yaml           # 本地配置含 Key（已 gitignore）
├── requirements.txt      # Python 依赖
├── main.py               # 入口
├── fetcher.py            # 数据抓取：RSS/ArXiv/HN/NewsAPI/WebSearch
├── processor.py          # AI 摘要生成
├── .gitignore
├── LICENSE
└── reports/              # 生成的日报（已 gitignore）
```

---

## 许可证

[MIT License](LICENSE) © 2026