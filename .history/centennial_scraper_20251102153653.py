import requests
from bs4 import BeautifulSoup

def get_centennial_campaign_impact(keyword="impact"):
    url = "https://www.xula.edu/about/centennial.html"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    found_lines = [ln for ln in lines if keyword.lower() in ln.lower()]
    if found_lines:
        return "\n".join(found_lines)

    return text[:500]

def search_page(keyword="impact"):
    url = "https://www.xula.edu/about/centennial.html"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    found_lines = [ln for ln in lines if keyword.lower() in ln.lower()]

    return "\n".join(found_lines) if found_lines else text[:500]

if __name__ == "__main__":
    print("Centennial Campaign Search ('exit' to quit)\n")
    while True:
        keyword = input("Enter keyword (or 'exit'): ").strip()
        if keyword.lower() == "exit":
            print("Goodbye!")
            break
        if not keyword:
            keyword = "impact"
        print(f"\n--- Searching for: {keyword} ---\n")
        print(search_page(keyword))
        print("\n" + "-"*50 + "\n")