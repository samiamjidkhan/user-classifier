import requests
from bs4 import BeautifulSoup

import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def scrape_website_content(url):
    # Check if cached
    cached_content = redis_client.get(url)
    if cached_content:
        return json.loads(cached_content)
    
    # If not cached, scrape
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    content = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
    
    # Cache scraped content
    redis_client.set(url, json.dumps(content), ex=3600)  # Cache for 1 hour
    return content

