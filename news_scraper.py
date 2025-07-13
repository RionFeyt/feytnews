import os
import requests
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Get the API key from your .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_headlines():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=50&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"News API error: {response.status_code}")
    
    articles = response.json().get("articles", [])
    headlines = [article["title"] for article in articles if article.get("title")]
    
    return headlines

# For testing purposes only
if __name__ == "__main__":
    headlines = fetch_headlines()
    for i, h in enumerate(headlines, 1):
        print(f"{i}. {h}")
