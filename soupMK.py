from bs4 import BeautifulSoup
import requests
import validators

class SoupMaker:
    def __init__(self, set_url=None, headers=None, debug=False):
        self.url = set_url
        self.debug = debug  
        self.headers = headers if headers is not None else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def is_valid_url(self, url):
        return validators.url(url)
    
    def makeSoup(self, url=None):
        target_url = url or self.url
        
        if not target_url:
            msg = "No URL provided."
            return self._handle_error(msg)
        
        if not self.is_valid_url(target_url):
            msg = f"Invalid URL format: {target_url}"
            return self._handle_error(msg)
        
        try:
            session = requests.Session()
            response = session.get(target_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                msg = f"Failed to load page (Status code: {response.status_code})"
                return self._handle_error(msg)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            if not soup:
                return self._handle_error("Failed to parse the page content.")
            
            print("Scrape was successful!")
            return soup
        
        except requests.RequestException as e:
            return self._handle_error(f"Request error: {e}")
        
        except Exception as e:
            return self._handle_error(f"Unexpected error: {e}")

    def _handle_error(self, message):
        if self.debug:
            raise Exception(message)  
        else:
            print(f" {message}")
            return None
    @staticmethod   
    def number_of_pages():
        num_pages = int(input("How many pages scrapped?"))
        while num_pages < 0:
            num_pages = int(input("Invaild input,how many pages scrapped?"))
        return num_pages