import os
import argparse
import numpy as np
from PIL import Image
from rembg import remove
import cv2
import insightface

def load_images(folder_path, main_image_name):
    images = []
    center_img = None
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder_path, filename)
            img = Image.open(path).convert("RGB")
            if filename == main_image_name:
                center_img = img
            else:
                images.append((filename, img))
    return center_img, images

def remove_background(image_pil):
    image_np = np.array(image_pil)
    output = remove(image_np)
    return Image.fromarray(output)

def auto_expand(image_pil, margin=50):
    w, h = image_pil.size
    new_img = Image.new("RGB", (w + 2*margin, h + 2*margin), (255, 255, 255))
    new_img.paste(image_pil, (margin, margin))
    return new_img

def create_grid(images, cell_width, cell_height, cols=5):
    rows = int(np.ceil(len(images) / cols))
    grid_img = Image.new("RGB", (cols * cell_width, rows * cell_height), (255, 255, 255))
    for idx, (_, img) in enumerate(images):
        img = auto_expand(img)
        img = img.resize((cell_width, cell_height))
        x = (idx % cols) * cell_width
        y = (idx // cols) * cell_height
        grid_img.paste(img, (x, y))
    return grid_img

def overlay_center_image(grid_img, center_img):
    center_img = remove_background(center_img).resize((500, 700))
    x = (grid_img.width - center_img.width) // 2
    y = (grid_img.height - center_img.height) // 2
    grid_img.paste(center_img, (x, y), center_img)
    return grid_img

def main(args):
    center_img, bg_imgs = load_images(args.images_folder, args.main_image)
    if not center_img:
        print("Main image not found!")
        return
    grid = create_grid(bg_imgs, 300, 500)
    final = overlay_center_image(grid, center_img)
    output_path = os.path.join("output", "final_collage.jpg")
    final.save(output_path)
    print(f"Collage saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_folder", type=str, default="images", help="Path to images folder")
    parser.add_argument("--main_image", type=str, required=True, help="Filename of the central image")
    args = parser.parse_args()
    main(args)
