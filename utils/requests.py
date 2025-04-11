import requests

def is_valid_image_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=5)
        return response.status_code == 200 and "image" in response.headers.get("Content-Type", "")
    except requests.RequestException:
        return False
