import sys
import yaml
from fetcher import fetch_all
from processor import process_articles


def load_config(path="config.yaml"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[Error] {path} not found. Copy config.example.yaml to config.yaml and fill in your API key.")
        sys.exit(1)


def main():
    config = load_config()

    provider = config.get("ai_provider", "anthropic")
    api_key = config.get("providers", {}).get(provider, {}).get("api_key", "")
    if not api_key:
        print(f"[Error] Set providers.{provider}.api_key in config.yaml to continue.")
        sys.exit(1)

    print("Fetching AI news...")
    articles = fetch_all(config)

    if not articles:
        print("[Warning] No articles fetched. Check network or source settings in config.yaml.")
        return

    print(f"Fetched {len(articles)} articles. Generating digest...")
    process_articles(articles, config)


if __name__ == "__main__":
    main()
