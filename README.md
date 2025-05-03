# Smart Photo Collage Generator

Python app to create a professional collage with one central image and multiple background images.

## Features
- Automatic background removal
- Face detection to avoid cropping
- Grid layout for background
- Auto expand (outpaint) if people are near edges
- Central image layered with transparency

## How to Use
1. Clone the repo
2. Place your images in the `images/` folder
3. Run:
```bash
python main.py --main_image "your_central_image.jpg"
```
4. Output saved to `output/final_collage.jpg`

## Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```
