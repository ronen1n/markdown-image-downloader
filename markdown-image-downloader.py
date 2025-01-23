import os
import re
import base64
import requests
from urllib.parse import urlparse
import argparse
from time import sleep

def parse_args():
    parser = argparse.ArgumentParser(description="Download images from a Markdown file.")
    parser.add_argument("-m", "--markdown", required=True, help="Path to the Markdown file")
    parser.add_argument("-f", "--folder", help="Folder name to save images (inside 'image/')")
    parser.add_argument("--base64", action="store_true", help="Convert images to base64 encoding")
    return parser.parse_args()

def download_image(url, image_path=None, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # If image_path is provided, save the file
                if image_path:
                    with open(image_path, 'wb') as img_file:
                        img_file.write(response.content)
                return response.content
            else:
                print(f"Failed to download: {url} (Status code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        
        if attempt < max_retries - 1:
            print(f"Retrying in 5 seconds... (Attempt {attempt + 2}/{max_retries})")
            sleep(5)
    
    return None

def get_image_mime_type(url):
    # Determine mime type based on file extension
    ext = os.path.splitext(urlparse(url).path)[1][1:].lower()
    mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'svg': 'image/svg+xml'
    }
    return mime_types.get(ext, 'image/jpeg')  # default to jpeg if unknown

def get_unique_file_name(directory, file_name):
    base_name, ext = os.path.splitext(file_name)
    unique_name = file_name
    counter = 1
    
    while os.path.exists(os.path.join(directory, unique_name)):
        unique_name = f"{base_name}_{counter:02}{ext}"
        counter += 1
    
    return unique_name
    
def main():
    args = parse_args()
    md_file = args.markdown

    if args.base64:
        # Remove folder requirement for base64
        if args.folder:
            print("Warning: --folder option is ignored when using --base64")
    else:
        # Maintain original behavior for non-base64 mode
        if not args.folder:
            print("Error: -f/--folder is required when not using --base64")
            return
        base_image_dir = os.path.join('image', args.folder)
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

        if args.base64:
            # Download and convert to base64
            image_content = download_image(clean_url)
            
            if image_content:
                mime_type = get_image_mime_type(clean_url)
                base64_image = base64.b64encode(image_content).decode('utf-8')
                base64_replacement = f"data:{mime_type};base64,{base64_image}"
                content = content.replace(url, base64_replacement)
                print(f"Converted to base64: {clean_url}")
            else:
                print(f"Failed to download: {clean_url}")
        else:
            # Original download and save behavior
            image_name = os.path.basename(urlparse(clean_url).path)
            unique_image_name = get_unique_file_name(base_image_dir, image_name)
            image_path = os.path.join(base_image_dir, unique_image_name)

            if download_image(clean_url, image_path):
                print(f"Downloaded: {unique_image_name}")
                relative_image_path = f"{args.folder}/{unique_image_name}".replace('\\', '/')
                content = content.replace(url, f"image/{relative_image_path}")
            else:
                print(f"Failed to download after multiple attempts: {url}")

    with open(md_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print("Markdown file updated.")

if __name__ == "__main__":
    main()