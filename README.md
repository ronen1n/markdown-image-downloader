# Markdown Image Downloader

Downloads external images referenced in a Markdown file to local image files or in base64 and updates the md to use the local image paths or the base64.

## Features

- Downloads images from URLs in Markdown files to **local image files**
- Updates image links in the Markdown to point to the local files
- Avoids overwriting existing images by creating unique filenames
- Save the files in **Base64** instead of image files
- Creates a backup of the original Markdown file

Example:

```
![alt text](https://github.com/image.png)
# to
![1694705809210](image/github/1694705809210.png)
# or in base64
![alt text](data:image/png;base64,the-base64-image)
```

## Installation

Python 3.6+

```
pip install requests

https://github.com/ronen1n/markdown-image-downloader.git
cd markdown-image-downloader
# or
curl https://raw.githubusercontent.com/ronen1n/markdown-image-downloader/refs/heads/main/markdown-image-downloader.py -o markdown-image-downloader.py
```

## Usage

Video: [markdown image downloader](https://www.youtube.com/watch?v=yNyocaFN6bY)

Run the script from the command line with the following arguments:

```
python markdown-image-downloader.py -m <markdown_file> -f <folder_name>
# or base64
python markdown-image-downloader.py -m <markdown_file> --base64
```

- `-m` or `--markdown`: Path to the Markdown file
- `-f` or `--folder`: Folder name to save images (inside 'image/<folder_name>')
- `--base64`: Convert images to base64 encoding

Example for downloading to local image files:

```
python markdown-image-downloader.py -m my_post.md -f blog_images
```

This will process `my_post.md`, download its images to `image/blog_images/`, and update the Markdown file with new local image paths.

## License

This project is open source and available under the [MIT License](LICENSE).

## Show your support

Give a ⭐️ if this project helped you!
