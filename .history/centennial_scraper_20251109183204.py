import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

def save_scraped_images(category="general"):
    url = "https://www.xula.edu/about/centennial.html"
    main_folder = "scrapped_assets"
    keyword = read_keyword_from_file()
    category_folder = os.path.join(main_folder, keyword, category)

    os.makedirs(category_folder, exist_ok=True)

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