from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/check_template")
def check_template(url: str = Query(..., description="Email template URL to check")):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content_length = len(response.text)
        return {
            "url": url,
            "status_code": response.status_code,
            "content_length": content_length,
            "message": "Template URL fetched successfully"
        }
    except requests.RequestException as e:
        return {
            "url": url,
            "error": str(e)
        }
