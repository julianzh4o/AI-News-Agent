import os
from datetime import date

LANG_NAMES = {
    "zh": "Chinese (Simplified)",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
}

DEFAULT_BASE_URLS = {
    "openai":    "https://api.openai.com/v1",
    "gemini":    "https://generativelanguage.googleapis.com/v1beta/openai/",
    "deepseek":  "https://api.deepseek.com/v1",
    "groq":      "https://api.groq.com/openai/v1",
    "moonshot":  "https://api.moonshot.cn/v1",
    "zhipu":     "https://open.bigmodel.cn/api/paas/v4",
    "qwen":      "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "mistral":   "https://api.mistral.ai/v1",
}


def _build_prompt(articles, top_n, lang_name):
    lines = []
    for i, a in enumerate(articles, 1):
        snippet = f" — {a['snippet'][:200]}" if a.get("snippet") else ""
        lines.append(f"{i}. [{a['source']}] {a['title']}{snippet}")
    return f"""You are an AI news curator. From the articles below, select {top_n} items (5–8 range) that cover any of these categories (skip a category if no relevant article exists):
1. Major product launches or feature updates (OpenAI, Google, Anthropic, Meta, etc.)
2. Funding events and industry M&A
3. Technical breakthroughs or notable paper releases
4. Industry standards and regulatory dynamics (AI safety frameworks, data governance)

Output language: {lang_name}

Output format (sorted by importance, most important first):
- For each item: **[Category] Title** | Source | One-sentence summary
- End with a "今日趋势点评" (or "Trend Commentary" in non-Chinese output) section: 2–3 sentences on the overall patterns visible today.
- Focus on technical progress and business dynamics. Skip entertainment or unrelated content.

Articles:
{chr(10).join(lines)}"""


def process_articles(articles, config):
    provider_name = config.get("ai_provider", "anthropic")
    provider_cfg = config.get("providers", {}).get(provider_name, {})
    api_key = provider_cfg.get("api_key", "")

    if not api_key:
        print(f"[Error] providers.{provider_name}.api_key is not set in config.yaml")
        return

    language = config.get("language", "zh")
    lang_name = LANG_NAMES.get(language, language)
    top_n = config.get("top_n", 10)
    model = provider_cfg.get("model", "")
    base_url = provider_cfg.get("base_url") or None
    prompt = _build_prompt(articles, top_n, lang_name)

    print("\n" + "=" * 60)
    chunks = []

    if provider_name == "anthropic":
        import anthropic
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        client = anthropic.Anthropic(**kwargs)
        with client.messages.stream(
            model=model or "claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                chunks.append(text)
    else:
        from openai import OpenAI
        effective_base_url = base_url or DEFAULT_BASE_URLS.get(provider_name)
        client = OpenAI(api_key=api_key, base_url=effective_base_url)
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            stream=True,
        )
        for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            print(text, end="", flush=True)
            chunks.append(text)

    print("\n" + "=" * 60)

    if config.get("save_report"):
        _save_report("".join(chunks), config)


def _save_report(content, config):
    report_dir = config.get("report_path", "reports/")
    os.makedirs(report_dir, exist_ok=True)
    filename = os.path.join(report_dir, f"ai-news-{date.today().isoformat()}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# AI News Digest — {date.today().isoformat()}\n\n{content}")
    print(f"\nReport saved: {filename}")
