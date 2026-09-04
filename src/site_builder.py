import json
import os

NEWS_FILE = "public/news.json"
MAX_NEWS_SIZE = 100

def load_public_news():
    """
    公開用の news.json を読み込みます。
    存在しない場合は空リストを返します。
    """
    if not os.path.exists(NEWS_FILE):
        return []
        
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def update_site_data(positive_articles):
    """
    AI判定を通過したポジティブな記事を、既存の公開データとマージします。
    新しい記事を先頭に追加し、最大件数を超えた古い記事は削除します。
    """
    if not positive_articles:
        print("No positive articles to add.")
        return
        
    existing_news = load_public_news()
    
    # 新しい記事を先頭に追加
    updated_news = positive_articles + existing_news
    
    # 最大件数でスライス（古い記事を押し出し）
    if len(updated_news) > MAX_NEWS_SIZE:
        updated_news = updated_news[:MAX_NEWS_SIZE]
        
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(NEWS_FILE), exist_ok=True)
    
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_news, f, ensure_ascii=False, indent=2)
        
    print(f"Site data updated. Added {len(positive_articles)} articles.")
