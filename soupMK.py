from bs4 import BeautifulSoup
import requests
import validators

class SoupMaker:
    def __init__(self, set_url=None, headers=None):
        self.url = set_url
        self.headers = headers if headers is not None else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def is_vaild_url(self, url):
        return validators.url(url)
    
    def makeSoup(self, url=None):
        if url is not None:
            target_url = url
        else:
            target_url = self.url
        
        if target_url is None:
            raise ValueError("No URL provided.")
        if self.is_vaild_url(target_url):
            try:
                
                session = requests.Session()
                response = session.get(target_url, headers=self.headers, timeout=10)
                if response.status_code != 200: #A response code of 200 indicates success
                    raise Exception(f"Failed to load page {target_url}, status code: {response.status_code}")
                
            except requests.RequestException as e:
                raise Exception(f"An error occurred while fetching the page: {e}")
        else:
            raise ValueError(f"Invalid URL format: {url}")
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        if soup is None:
            raise Exception("Failed to parse the page content.")
        print('Scrape was successful' )
        return soup
    
    
    
amazon = SoupMaker("https://www.amazon.com/s?k=")
amazon.makeSoup(amazon.url)


