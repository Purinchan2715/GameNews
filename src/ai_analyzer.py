import os
import json
import time
import re
import google.generativeai as genai
from dotenv import load_dotenv

# ローカルテスト用に .env ファイルから環境変数を読み込む
load_dotenv()

# Gemini APIの初期設定
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def analyze_articles(articles):
    """
    新規記事をGemini APIに送信し、ネガティブ判定を行います。
    APIコール節約のため、チャンクに分けて処理します。
    """
    if not api_key:
        print("Warning: GEMINI_API_KEY is not set. Skipping AI analysis and treating all as positive.")
        return articles

    positive_articles = []
    chunk_size = 5 # 1リクエストで判定する記事数
    
    # 使用するモデル。軽量で高速な gemini-1.5-flash を利用
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    for i in range(0, len(articles), chunk_size):
        chunk = articles[i:i + chunk_size]
        print(f"Analyzing chunk {i//chunk_size + 1} ({len(chunk)} articles)...")
        
        # APIに送信する入力データを作成
        input_data = []
        for idx, article in enumerate(chunk):
            input_data.append({
                "id": idx,
                "title": article["title"],
                "summary": article["summary"][:200] # 要約が長すぎる場合は切り詰める
            })
            
        prompt = f"""
あなたはゲームニュースの感情アナリストです。
以下のJSON形式で提供される複数のゲームニュースを分析し、ユーザーを不快にさせるネガティブな要素（サービス終了、発売延期、重篤なバグ、炎上、不祥事、リストラなど）が含まれているか、記事ごとに判定してください。

【入力データ】
{json.dumps(input_data, ensure_ascii=False)}

【出力フォーマット】
必ず以下のJSON配列形式のみを出力してください。Markdownのコードブロック(```json)は不要です。
[
  {{"id": 0, "is_negative": false}},
  {{"id": 1, "is_negative": true}}
]
"""
        try:
            response = model.generate_content(prompt)
            # Markdownのコードブロックが含まれている場合の対策として正規表現で抽出
            match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if match:
                result_json = match.group(0)
            else:
                result_json = response.text
                
            results = json.loads(result_json)
            
            # 結果を元にポジティブな記事だけをリストに追加
            for res in results:
                if not res.get("is_negative", True):
                    positive_articles.append(chunk[res["id"]])
                    
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            # エラー時は安全側に倒し、このチャンクはスキップ（ポジティブに追加しない）
            pass
            
        # レートリミット対策（API呼び出しの間に少し待機）
        time.sleep(3)
        
    return positive_articles
