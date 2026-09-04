import json
import os
import sys

# srcディレクトリ内のモジュールをインポートするためにパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetcher import fetch_rss_feeds
from history_manager import load_history, filter_new_articles, save_history
from ai_analyzer import analyze_articles
from site_builder import update_site_data

CONFIG_FILE = "src/config.json"

def main():
    """
    システムのメイン実行エントリーポイントです。
    GitHub Actionsやローカル環境からこのスクリプトが最初に呼び出されます。
    """
    print("=== System Started ===")
    
    # 1. 設定の読み込み
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            rss_urls = config.get("rss_feeds", [])
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    if not rss_urls:
        print("No RSS feeds configured.")
        return

    # 2. 記事の収集
    print("\n--- Phase 1: Fetching ---")
    all_articles = fetch_rss_feeds(rss_urls)
    
    # 3. 差分（新規記事）の抽出
    print("\n--- Phase 2: Diffing ---")
    history_urls = load_history()
    new_articles = filter_new_articles(all_articles, history_urls)
    print(f"Found {len(new_articles)} new articles.")
    
    if not new_articles:
        print("No new articles to process. Exiting.")
        return

    # 4. AIによるネガティブ判定
    print("\n--- Phase 3: AI Analysis ---")
    positive_articles = analyze_articles(new_articles)
    print(f"{len(positive_articles)} articles passed the AI filter.")

    # 5. データ更新とサイト用ファイルの生成
    print("\n--- Phase 4: Updating Site & History ---")
    update_site_data(positive_articles)
    
    # 新しく処理したすべてのURLを履歴に保存 (ポジティブ/ネガティブ問わず)
    new_urls = [article["url"] for article in new_articles]
    save_history(history_urls, new_urls)
    
    print("\n=== System Finished ===")

if __name__ == "__main__":
    main()
