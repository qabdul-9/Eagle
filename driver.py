from bs4 import BeautifulSoup
import requests
from scraper import AmazonImageScraper


def main():
    url = "https://www.amazon.com/s?k="
    scraper = AmazonImageScraper(url, headers=None)

    usrinput = input("Enter the product you want to search for on Amazon: ")
    url += usrinput.replace(" ", "+") #Replace spaces with '+' for URL encoding

    
    soup = scraper.makeSoup(url)

    

    
    print(f"Page Title: {soup.title}")
    print(soup.prettify()[:1000])


if __name__ == "__main__":
    main()