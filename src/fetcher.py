import feedparser
import time

def fetch_rss_feeds(urls):
    """
    指定された複数のRSS URLから記事を取得し、リストにまとめて返します。
    """
    articles = []
    
    for url in urls:
        print(f"Fetching RSS: {url}")
        # feedparserを使ってRSSを取得・解析
        feed = feedparser.parse(url)
        
        # 記事(entry)ごとに必要な情報を抽出
        for entry in feed.entries:
            article = {
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                # summaryがない場合はdescriptionを代用
                "summary": entry.get("summary", entry.get("description", "")),
                "published_at": entry.get("published", entry.get("updated", "")),
                "source_site": feed.feed.get("title", "Unknown Source")
            }
            articles.append(article)
            
    print(f"Total {len(articles)} articles fetched.")
    return articles
