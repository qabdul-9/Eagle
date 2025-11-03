from bs4 import BeautifulSoup
import requests
class SoupMaker:
    def __init__(self, set_url, headers=None):
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

    @staticmethod
    def makeSoup(self, url=None):
        target_url = url if url is not None else self.url
        try:
            session = requests.Session()
            response = session.get(target_url, headers=self.headers, timeout=10)
            if response.status_code != 200: #A response code of 200 indicates success
                raise Exception(f"Failed to load page {target_url}, status code: {response.status_code}")
            
        except requests.RequestException as e:
            raise Exception(f"An error occurred while fetching the page: {e}")
        
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        if soup is None:
            raise Exception("Failed to parse the page content.")
        
        return soup
    
    
