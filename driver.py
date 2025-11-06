from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import validators 

def is_vaild_url(url):
    return validators.url(url)

def fetch_page(url, headers=None):
    if is_vaild_url(url):
        response = requests.get(url, headers=headers)
        if response.status_code != 200: #A response code of 200 indicates success
            raise Exception(f"Failed to load page {url}, status code: {response.status_code}")
        
        return response.text
    raise ValueError(f"Invalid URL format: {url}")

def main():
    url = "https://www.amazon.com/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
    }
    
    page_content = fetch_page(url, headers=headers)
    soup = BeautifulSoup(page_content, 'html.parser')
    if(soup is None):
        print("Failed to parse the page content.")
        return
    else:
        title = soup.title.string
    
    print(f"Page Title: {title}")
    print(soup.prettify()[:1000])


if __name__ == "__main__":
    main()