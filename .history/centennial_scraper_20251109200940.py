import requests
from bs4 import BeautifulSoup
from image_scraper import save_scraped_images


def get_centennial_campaign_impact():
    url = "https://www.xula.edu/about/centennial.html"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    lines = []
    for line in text.splitlines():
        clean_line = line.strip()
        if clean_line:
            lines.append(clean_line)
    return lines


def search_page(keyword="impact"):
    lines = get_centennial_campaign_impact()
    if not lines:
        return "Error: Could not retrieve page content."
    
    found_lines = []
    for line in lines:
        if keyword.lower() in line.lower():
            found_lines.append(line)
    if len(found_lines) > 0:
        return "\n".join(found_lines)
    else:
        return "\n".join(lines[:20])


if __name__ == "__main__":
    print("Centennial Campaign Search ('exit' to quit, 'saveimg' to download images)\n")
    while True:
        try:
            keyword = input("Enter keyword: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
            
        if keyword.lower() == "exit":
            print("Goodbye!")
            break
        elif keyword.lower() == "saveimg":
            try:
                category = input("Enter category name for images: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nCancelled.")
                continue
            if category == "":
                category = "general"
            save_scraped_images(category)
            continue
        elif keyword == "":
            keyword = "impact"
        print("\n--- Searching for:", keyword, "---\n")
        print(search_page(keyword))
        print("\n" + "-" * 50 + "\n")