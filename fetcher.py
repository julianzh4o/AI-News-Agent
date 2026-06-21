import feedparser
import httpx
import urllib.parse
import xml.etree.ElementTree as ET


def _rss_entry(entry, source_name):
    return {
        "title": entry.get("title", "").strip(),
        "url": entry.get("link", ""),
        "snippet": entry.get("summary", "")[:300],
        "source": source_name,
        "published": entry.get("published", ""),
    }


def fetch_rss(feeds):
    articles = []
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:5]:
                articles.append(_rss_entry(entry, feed["name"]))
        except Exception:
            pass
    return articles


def fetch_arxiv(cfg):
    query = urllib.parse.quote(cfg.get("query", "artificial intelligence"))
    max_results = cfg.get("max_results", 20)
    url = (
        f"https://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={max_results}"
    )
    try:
        resp = httpx.get(url, timeout=15)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(resp.text)
        articles = []
        for entry in root.findall("atom:entry", ns):
            title = entry.findtext("atom:title", "", ns).replace("\n", " ").strip()
            link = next(
                (l.get("href") for l in entry.findall("atom:link", ns) if l.get("type") == "text/html"),
                "",
            )
            summary = entry.findtext("atom:summary", "", ns)[:300]
            published = entry.findtext("atom:published", "", ns)
            articles.append({"title": title, "url": link, "snippet": summary, "source": "ArXiv", "published": published})
        return articles
    except Exception:
        return []


def fetch_hackernews(cfg):
    min_points = cfg.get("min_points", 50)
    max_results = cfg.get("max_results", 15)
    url = (
        f"https://hn.algolia.com/api/v1/search"
        f"?query=AI+artificial+intelligence&tags=story"
        f"&numericFilters=points>{min_points}&hitsPerPage={max_results}"
    )
    try:
        data = httpx.get(url, timeout=10).json()
        return [
            {
                "title": h.get("title", ""),
                "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                "snippet": "",
                "source": "HackerNews",
                "published": h.get("created_at", ""),
            }
            for h in data.get("hits", [])
        ]
    except Exception:
        return []


def fetch_newsapi(cfg, api_key):
    query = urllib.parse.quote(cfg.get("query", "artificial intelligence"))
    max_results = cfg.get("max_results", 20)
    lang = cfg.get("language", "en")
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={query}&language={lang}&sortBy=publishedAt"
        f"&pageSize={max_results}&apiKey={api_key}"
    )
    try:
        data = httpx.get(url, timeout=10).json()
        return [
            {
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "snippet": (a.get("description") or "")[:300],
                "source": a.get("source", {}).get("name", "NewsAPI"),
                "published": a.get("publishedAt", ""),
            }
            for a in data.get("articles", [])
            if a.get("title") and "[Removed]" not in a.get("title", "")
        ]
    except Exception:
        return []


def fetch_websearch(cfg):
    engine = cfg.get("engine", "duckduckgo")
    query = cfg.get("query", "AI artificial intelligence latest news")
    max_results = cfg.get("max_results", 10)

    if engine == "duckduckgo":
        try:
            from ddgs import DDGS
            return [
                {"title": r["title"], "url": r["href"], "snippet": r.get("body", "")[:300],
                 "source": "DuckDuckGo", "published": ""}
                for r in DDGS().text(query, max_results=max_results)
            ]
        except Exception:
            return []

    if engine == "tavily":
        api_key = cfg.get("tavily_api_key", "")
        if not api_key:
            return []
        try:
            data = httpx.post(
                "https://api.tavily.com/search",
                json={"api_key": api_key, "query": query, "max_results": max_results},
                timeout=15,
            ).json()
            return [
                {"title": r.get("title", ""), "url": r.get("url", ""),
                 "snippet": r.get("content", "")[:300], "source": "Tavily",
                 "published": r.get("published_date", "")}
                for r in data.get("results", [])
            ]
        except Exception:
            return []

    if engine == "serpapi":
        api_key = cfg.get("serpapi_api_key", "")
        if not api_key:
            return []
        try:
            data = httpx.get(
                "https://serpapi.com/search",
                params={"q": query, "api_key": api_key, "num": max_results, "engine": "google"},
                timeout=15,
            ).json()
            return [
                {"title": r.get("title", ""), "url": r.get("link", ""),
                 "snippet": r.get("snippet", "")[:300], "source": "SerpAPI", "published": ""}
                for r in data.get("organic_results", [])
            ]
        except Exception:
            return []

    return []


def fetch_all(config):
    articles = []
    sources = config.get("sources", {})

    if sources.get("rss"):
        articles += fetch_rss(config.get("rss_feeds", []))
    if sources.get("arxiv"):
        articles += fetch_arxiv(config.get("arxiv", {}))
    if sources.get("hackernews"):
        articles += fetch_hackernews(config.get("hackernews", {}))

    newsapi_key = config.get("newsapi_key", "")
    if sources.get("newsapi") and newsapi_key:
        articles += fetch_newsapi(config.get("newsapi", {}), newsapi_key)
    if sources.get("websearch"):
        articles += fetch_websearch(config.get("websearch", {}))

    seen, unique = set(), []
    for a in articles:
        if a["title"] and a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    return unique
