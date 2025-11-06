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
    url = "https://www.amazon.com/s?k="
    scraper = SoupMaker(url, headers=None)

    usrinput = input("Enter the product you want to search for on Amazon: ")
    url += usrinput.replace(" ", "+") #Replace spaces with '+' for URL encoding

    
    soup = scraper.makeSoup(url)

    

    
    print(f"Page Title: {soup.title}")
    print(soup.prettify()[:1000])


if __name__ == "__main__":
    main()