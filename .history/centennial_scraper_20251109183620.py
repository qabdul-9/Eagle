import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

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

def read_keyword_from_file():
    filename = "keyword.txt"
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                keyword = f.read().strip()
                if keyword:
                    return keyword
    except Exception as e:
        print(f"Error reading keyword file: {e}")
    return "default"

def save_scraped_images(category="general"):
    url = "https://www.xula.edu/about/centennial.html"
    main_folder = "scrapped_assets"
    keyword = read_keyword_from_file()
    category_folder = os.path.join(main_folder, keyword, category)

    try:
        os.makedirs(category_folder, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    print(f"Found {len(images)} images.")
    
    if len(images) == 0:
        print("No images found on the page.")
        return
    
    count = 1
    successful = 0
    
    for img in images:
        src = img.get("src")
        if not src:
            print(f"Skipping image {count}: No src attribute")
            continue
            
        image_url = urljoin(url, src)
        
        try:
            img_response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            img_response.raise_for_status()
            
            extension = Path(image_url).suffix
            if not extension or extension == '':
                content_type = img_response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    extension = '.jpg'
                elif 'png' in content_type:
                    extension = '.png'
                elif 'gif' in content_type:
                    extension = '.gif'
                elif 'webp' in content_type:
                    extension = '.webp'
                else:
                    extension = '.jpg'
            
            filename = f"image_{count}{extension}"
            path = os.path.join(category_folder, filename)
            
            with open(path, "wb") as file:
                file.write(img_response.content)
            
            print(f"✓ Saved: {path}")
            successful += 1
            
        except requests.RequestException as e:
            print(f"✗ Error downloading {image_url}: {e}")
        except Exception as e:
            print(f"✗ Error saving image {count}: {e}")
        
        count += 1
    
    print(f"\nProcessed {count-1} images, successfully saved {successful}.\n")

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