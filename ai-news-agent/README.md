# AI News Agent

A CLI tool that collects global AI news from multiple sources and generates a structured daily digest using your preferred LLM.

## Features

- **5 data sources**: RSS feeds, ArXiv papers, HackerNews, NewsAPI, Web Search (DuckDuckGo/Tavily/SerpAPI)
- **9 AI providers**: Anthropic, OpenAI, Gemini, DeepSeek, Groq, Moonshot, Zhipu, Qwen, Mistral
- **Custom relay/proxy support**: set a `base_url` per provider for third-party API gateways
- **Multilingual output**: zh, en, ja, ko, fr, de, es, ru, and more
- **Structured digest**: categorized by product launches, funding, research breakthroughs, and regulatory news

## Quickstart

```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml   # then edit config.yaml
python main.py
```

## Configuration

Edit `config.yaml`:

```yaml
ai_provider: "anthropic"   # which LLM to use

providers:
  anthropic:
    api_key: "sk-ant-..."  # your API key
    base_url: ""           # optional: relay/proxy URL
    model: "claude-sonnet-4-6"

language: "zh"             # output language
```

All available options and their defaults are documented inside `config.yaml`.

### Supported AI providers

| Provider | Default model | Notes |
|----------|--------------|-------|
| `anthropic` | claude-sonnet-4-6 | [console.anthropic.com](https://console.anthropic.com) |
| `openai` | gpt-4o | [platform.openai.com](https://platform.openai.com) |
| `gemini` | gemini-2.0-flash | [aistudio.google.com](https://aistudio.google.com) |
| `deepseek` | deepseek-chat | [platform.deepseek.com](https://platform.deepseek.com) |
| `groq` | llama-3.3-70b-versatile | [console.groq.com](https://console.groq.com) |
| `moonshot` | moonshot-v1-8k | [platform.moonshot.cn](https://platform.moonshot.cn) |
| `zhipu` | glm-4-flash | [open.bigmodel.cn](https://open.bigmodel.cn) |
| `qwen` | qwen-plus | [dashscope.aliyun.com](https://dashscope.aliyun.com) |
| `mistral` | mistral-large-latest | [console.mistral.ai](https://console.mistral.ai) |

### Web search engines

| Engine | API key required |
|--------|-----------------|
| `duckduckgo` | No (default) |
| `tavily` | Yes — [tavily.com](https://tavily.com) |
| `serpapi` | Yes — [serpapi.com](https://serpapi.com) |

## Output format

```
[产品发布] GPT-5 发布 | OpenAI | 一句话摘要
[融资并购]  ...
...
今日趋势点评: ...
```

## License

MIT
