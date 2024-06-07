
import requests
from bs4 import BeautifulSoup

def fetch_main_body_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if title_tag and meta_tag:
            title = title_tag.get_text() if title_tag else ''
            description = meta_tag.get('content') if meta_tag else ''
            return title, description
        else:
            raise Exception("Title or meta description not found on the page.")
    else:
        raise Exception(f"Failed to fetch data from {url}")
