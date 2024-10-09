# Downloads external link images in markdown file to local folder and change the image link in md to the local images files
#
# The image needs to be in the right format `![](https...)`
# python markdown-image-downloader.py -m "file_name.md" -f "image_folder"

import os
import re
import requests
from urllib.parse import urlparse
import argparse
from time import sleep

def get_unique_file_name(directory, file_name):
    base_name, ext = os.path.splitext(file_name)
    unique_name = file_name
    counter = 1
    
    while os.path.exists(os.path.join(directory, unique_name)):
        unique_name = f"{base_name}_{counter:02}{ext}"
        counter += 1
    
    return unique_name

def parse_args():
    parser = argparse.ArgumentParser(description="Download images from a Markdown file.")
    parser.add_argument("-m", "--markdown", required=True, help="Path to the Markdown file")
    parser.add_argument("-f", "--folder", required=True, help="Folder name to save images (inside 'image/')")
    return parser.parse_args()

def download_image(url, image_path, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                return True
            else:
                print(f"Failed to download: {url} (Status code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        
        if attempt < max_retries - 1:
            print(f"Retrying in 5 seconds... (Attempt {attempt + 2}/{max_retries})")
            sleep(5)
    
    return False

def main():
    args = parse_args()
    md_file = args.markdown
    folder_name = args.folder
    base_image_dir = os.path.join('image', folder_name)
    os.makedirs(base_image_dir, exist_ok=True)

    image_pattern = r'!\[.*?\]\((https?://.*?)\)'

    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()

    image_urls = re.findall(image_pattern, content)

    backup_md_file = md_file.replace('.md', '_backup.md')
    with open(backup_md_file, 'w', encoding='utf-8') as backup_file:
        backup_file.write(content)

    for url in image_urls:
        # Remove query parameters
        clean_url = url.split('?')[0]
        image_name = os.path.basename(urlparse(clean_url).path)
        unique_image_name = get_unique_file_name(base_image_dir, image_name)
        image_path = os.path.join(base_image_dir, unique_image_name)

        if download_image(url, image_path):
            print(f"Downloaded: {unique_image_name}")
            # Use forward slashes and remove 'image' from the path
            relative_image_path = f"{folder_name}/{unique_image_name}".replace('\\', '/')
            content = content.replace(url, f"image/{relative_image_path}")
        else:
            print(f"Failed to download after multiple attempts: {url}")

    with open(md_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print("Markdown file updated with new image paths.")

if __name__ == "__main__":
    main()
