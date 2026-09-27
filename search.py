import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def search_company(query, max_results=5):
    """
    Serper.dev API se Google search results nikaalta hai. Reliable, no blocking.
    Returns: (results_list, error_message)
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": f"{query} company OR business official website news", "num": max_results}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code != 200:
            return [], f"API Error. Status: {response.status_code}, Response: {response.text[:200]}"

        data = response.json()
        organic = data.get("organic", [])

        if not organic:
            return [], "Koi organic results nahi mile is query ke liye."

        results = []
        for item in organic[:max_results]:
            results.append({
                "title": item.get("title", ""),
                "href": item.get("link", ""),
                "body": item.get("snippet", "")
            })

        return results, None

    except Exception as e:
        return [], f"{type(e).__name__}: {str(e)}"


def scrape_page_text(url, max_chars=2000):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:max_chars]
    except Exception as e:
        return f"[Could not fetch content: {e}]"