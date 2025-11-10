import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_centennial_campaign_impact():
    url = "https://www.xula.edu/about/centennial.html"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
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
    found_lines = []
    for line in lines:
        if keyword.lower() in line.lower():
            found_lines.append(line)
    if len(found_lines) > 0:
        return "\n".join(found_lines)
    else:
        return "\n".join(lines[:20])

def read_keyword_from_file():
    filename = "keyword.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            keyword = f.read().strip()
            if keyword:
                return keyword
    return "default"

def save_scraped_images(category="general"):
    url = "https://www.xula.edu/about/centennial.html"
    main_folder = "scrapped_assets"
    keyword = read_keyword_from_file()
    category_folder = os.path.join(main_folder, keyword, category)

    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    print("Found", len(images), "images.")
    count = 1
    for img in images:
        src = img.get("src")
        if not src:
            continue
        image_url = urljoin(url, src)
        try:
            image_data = requests.get(image_url).content
            filename = f"image_{count}.jpg"
            path = os.path.join(category_folder, filename)
            with open(path, "wb") as file:
                file.write(image_data)
            print("Saved:", path)
            count += 1
        except Exception as e:
            print("Error saving image:", e)
    print("All images processed.\n")

if __name__ == "__main__":
    print("Centennial Campaign Search ('exit' to quit, 'saveimg' to download images)\n")
    while True:
        keyword = input("Enter keyword: ").strip()
        if keyword.lower() == "exit":
            print("Goodbye!")
            break
        elif keyword.lower() == "saveimg":
            category = input("Enter category name for images: ").strip()
            if category == "":
                category = "general"
            save_scraped_images(category)
            continue
        elif keyword == "":
            keyword = "impact"
        print("\n--- Searching for:", keyword, "---\n")
        print(search_page(keyword))
        print("\n" + "-" * 50 + "\n")
