import requests
from bs4 import BeautifulSoup

def get_centennial_info():
    url = "https://www.xula.edu/about/centennial.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    info = soup.get_text()
    return info

if __name__ == "__main__":
    text = get_centennial_info()
    print(text)
