import requests
from bs4 import BeautifulSoup

def scrape_centennial_campaign_impact():
    """
    Scrapes the Centennial Campaign Impact section text from XULA's website.
    Returns the text content as a string, or None if not found.
    """
    url = "https://www.xula.edu/about/centennial.html"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # raise error if page fails to load

        soup = BeautifulSoup(response.text, "html.parser")

        # Look for a section or header that contains “Centennial Campaign Impact”
        section = soup.find(lambda tag: tag.name in ["h2", "h3"] and "Impact" in tag.get_text())

        if not section:
            return None

        # Get the text following that section (paragraphs, divs, etc.)
        impact_text = []
        for sibling in section.find_next_siblings():
            if sibling.name in ["h2", "h3"]:  # stop at next section
                break
            text = sibling.get_text(strip=True)
            if text:
                impact_text.append(text)

        return "\n".join(impact_text) if impact_text else None

    except Exception as e:
        print(f"Error scraping Centennial Campaign Impact: {e}")
        return None
