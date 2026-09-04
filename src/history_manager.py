import json
import os

HISTORY_FILE = "src/history.json"
MAX_HISTORY_SIZE = 1000

def load_history():
    """
    history.json から処理済みURLのリストを読み込みます。
    ファイルが存在しない場合は空のリストを返します。
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def filter_new_articles(articles, history_urls):
    """
    取得した記事リストの中から、履歴(history.json)に存在しない新規記事のみを抽出します。
    """
    new_articles = []
    for article in articles:
        if article["url"] not in history_urls:
            new_articles.append(article)
    return new_articles

def save_history(history_urls, new_urls):
    """
    既存の履歴に新規処理したURLを追加し、history.json に保存します。
    ファイルサイズ肥大化を防ぐため、最新のもの(MAX_HISTORY_SIZE件)だけ残します。
    """
    updated_history = history_urls + new_urls
    
    # 履歴が最大サイズを超えた場合、古いものを切り捨てる
    if len(updated_history) > MAX_HISTORY_SIZE:
        updated_history = updated_history[-MAX_HISTORY_SIZE:]
        
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_history, f, ensure_ascii=False, indent=2)
