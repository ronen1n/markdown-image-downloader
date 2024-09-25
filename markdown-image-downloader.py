# Downloads external link images in markdown file to local folder and change the image link in md to the local images files
#
# The image needs to be in the right format `![](https...)`
# python markdown-image-downloader.py -m "file_name.md" -f "image_folder"

import os
import re
import requests
from urllib.parse import urlparse
import argparse

# Function to avoid overwriting files with the same name
def get_unique_file_name(directory, file_name):
    base_name, ext = os.path.splitext(file_name)
    counter = 1
    unique_name = file_name
    
    while os.path.exists(os.path.join(directory, unique_name)):
        unique_name = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return unique_name

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Download images from a Markdown file.")
    parser.add_argument("-m", "--markdown", required=True, help="Path to the Markdown file")
    parser.add_argument("-f", "--folder", required=True, help="Folder name to save images (inside 'image/')")
    return parser.parse_args()

def main():
    # Parse the command-line arguments
    args = parse_args()
    md_file = args.markdown
    folder_name = args.folder

    # Define the base directory for images
    base_image_dir = os.path.join('image', folder_name)

    # Create the image directory if it doesn't exist
    os.makedirs(base_image_dir, exist_ok=True)

    # Regex to find image URLs in the Markdown
    image_pattern = r'!\[.*?\]\((https?://.*?)\)'

    # Read the Markdown file
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all image URLs
    image_urls = re.findall(image_pattern, content)

    # Create a backup of the original Markdown file
    backup_md_file = md_file.replace('.md', '_backup.md')
    with open(backup_md_file, 'w', encoding='utf-8') as backup_file:
        backup_file.write(content)

    # Download images and update Markdown content
    for url in image_urls:
        # Extract the file name from the URL
        image_name = os.path.basename(urlparse(url).path)

        # Get a unique file name to avoid overwriting
        unique_image_name = get_unique_file_name(base_image_dir, image_name)
        image_path = os.path.join(base_image_dir, unique_image_name)

        # Download and save the image
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Downloaded: {unique_image_name}")

                # Replace the image URL in the Markdown content
                relative_image_path = f"{base_image_dir}/{unique_image_name}"
                content = content.replace(url, relative_image_path)

            else:
                print(f"Failed to download: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    # Write the updated content back to the Markdown file
    with open(md_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print("Markdown file updated with new image paths.")

if __name__ == "__main__":
    main()
