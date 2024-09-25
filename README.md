# Markdown Image Downloader

Downloads external images referenced in a Markdown file and updates the md to use the local image paths.

## Features

- Downloads images from URLs in Markdown files
- Updates image links in the Markdown to point to local files
- Avoids overwriting existing images by creating unique filenames
- Creates a backup of the original Markdown file

Example:

```
![alt text](https://github.com/image.png)
# to
![1694705809210](image/github/1694705809210.png)
```

## Installation

Python 3.6+

```
pip install requests

https://github.com/ronen1n/markdown-image-downloader.git
cd markdown-image-downloader
# or
curl https://raw.githubusercontent.com/ronen1n/markdown-image-downloader/refs/heads/main/markdown-image-downloader.py -o markdown-image-downloader.py

python markdown-image-downloader.py -m <markdown_file> -f <folder_name>
```

## Usage

Run the script from the command line with the following arguments:

```
python markdown-image-downloader.py -m <markdown_file> -f <folder_name>
```

- `-m` or `--markdown`: Path to the Markdown file
- `-f` or `--folder`: Folder name to save images (inside 'image/<folder_name>')

Example:

```
python markdown-image-downloader.py -m my_post.md -f blog_images
```

This will process `my_post.md`, download its images to `image/blog_images/`, and update the Markdown file with new local image paths.

## License

This project is open source and available under the [MIT License](LICENSE).

## Show your support

Give a ⭐️ if this project helped you!
