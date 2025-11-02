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
