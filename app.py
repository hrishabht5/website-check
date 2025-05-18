from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/check_template")
def check_template(url: str = Query(..., description="URL of the email template to check")):
    try:
        resp = requests.get(url, timeout=10)
        html = resp.text.lower()

        img_count = html.count("<img")
        p_count = html.count("<p")
        span_count = html.count("<span")

        result = {
            "has_unsubscribe": "unsubscribe" in html,
            "has_address": any(word in html for word in ["street", "road", "city", "zip", "pincode", "india"]),
            "has_title_tag": "<title>" in html and "</title>" in html,
            "has_viewport_meta": 'name="viewport"' in html,
            "has_spammy_words": any(word in html for word in ["free!!!", "act now", "limited time", "buy now", "guaranteed", "no cost"]),
            "image_to_text_ratio_warning": img_count > (p_count + span_count)
        }
        return {"template_url": url, "checks": result}
    except Exception as e:
        return {"error": str(e)}
