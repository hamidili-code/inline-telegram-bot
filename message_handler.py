import html
import requests

def process_inline_query(inline_data, bot_token):
    query_id = inline_data["id"]
    search_text = inline_data["query"].strip()
    results = []

    if search_text:
        try:
            search_api = f"https://shelow.ir/wp-json/shelow/v1/posts?search={requests.utils.quote(search_text)}&_embed"
            res = requests.get(search_api, timeout=5)

            if res.status_code == 200:
                posts = res.json()
                if isinstance(posts, list):
                    for post in posts[:5]:
                        clean_title = html.unescape(post.get("title", {}).get("rendered", ""))
                        link = post.get("link", "")

                        img_url = None
                        try:
                            img_url = post["_embedded"]["wp:featuredmedia"][0]["source_url"]
                        except (KeyError, IndexError, TypeError):
                            pass

                        results.append({
                            "type": "article",
                            "id": str(post["id"]),
                            "title": clean_title,
                            "input_message_content": {
                                "message_text": f"<b>{clean_title}</b>\n\n{link}",
                                "parse_mode": "HTML"
                            },
                            "description": f"مشاهده مقاله در {site_url}",
                            "thumb_url": img_url
                        })
        except Exception as e:
            print(f"Error in search: {e}")

    # ارسال پاسخ به تلگرام
    requests.post(f"https://api.telegram.org/bot{bot_token}/answerInlineQuery", json={
        "inline_query_id": query_id,
        "results": results,
        "cache_time": 1
    })