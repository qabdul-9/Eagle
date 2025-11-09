from bs4 import BeautifulSoup
import requests
import validators
import os

class SoupMaker:
    def __init__(self, set_url=None, headers=None, debug=False):
        self.url = set_url
        self.debug = debug
        self.errors = []          
        self.images_scraped = 0   
        self.save_folder = "images"  
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
            return self._handle_error("No URL provided.")
        
        if not self.is_valid_url(target_url):
            return self._handle_error(f"Invalid URL format: {target_url}")
        
        try:
            session = requests.Session()
            response = session.get(target_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return self._handle_error(f"Failed to load page (Status code: {response.status_code})")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            if not soup:
                return self._handle_error("Failed to parse the page content.")
            
            print("Scrape was successful!")
            return soup
        
        except requests.RequestException as e:
            return self._handle_error(f"Request error: {e}")
        
        except Exception as e:
            return self._handle_error(f"Unexpected error: {e}")
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
    
    def number_of_pages():
        num_pages = int(input("How many pages scrapped?"))
        while num_pages < 0:
            num_pages = int(input("Invaild input,how many pages scrapped?"))
        return num_pages 

    
amazon = SoupMaker("https://www.amazon.com/s?k=")
amazon.makeSoup(amazon.url)

    def scrape_images(self, soup, limit=10):
        """Example image scraping method."""
        if soup is None:
            return self._handle_error("No soup provided for scraping.")
        
        
        os.makedirs(self.save_folder, exist_ok=True)
        
        
        images = soup.find_all("img")
        print(f"Found {len(images)} images on the page.")
        
        
        for i, img in enumerate(images[:limit], start=1):
            src = img.get("src")
            if not src:
                continue
            try:
                img_data = requests.get(src).content
                file_name = os.path.join(self.save_folder, f"image_{i}.jpg")
                with open(file_name, "wb") as f:
                    f.write(img_data)
                self.images_scraped += 1
            except Exception as e:
                self._handle_error(f"Failed to download image {i}: {e}")
        
 
    def _handle_error(self, message):
        """Handle errors depending on debug mode."""
        self.errors.append(message) 
        if self.debug:
            raise Exception(message)
        else:
            print(f"{message}")
            return None

    @staticmethod
    def number_of_pages():
        num_pages = int(input("How many pages scraped? "))
        while num_pages < 0:
            num_pages = int(input("Invalid input, how many pages scraped? "))
        return num_pages
   def print_summary(self):
        print("\n=== SCRAPE SUMMARY ===")
        print(f"Images scraped: {self.images_scraped}")
        print(f"Saved to folder: {os.path.abspath(self.save_folder)}")
        print(f"Total errors: {len(self.errors)}")
        if self.errors:
            print("\nError details:")
            for err in self.errors:
                print(f" - {err}")
        print("=========================\n")
