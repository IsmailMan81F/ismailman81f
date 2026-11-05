import sys
import cv2
import numpy as np
from PIL import Image

try:
    from rembg import remove
except ImportError:
    remove = None

def prep_photo(input_path, output_path="source-prepped.png"):
    img_pil = Image.open(input_path)
    if remove:
        img_pil = remove(img_pil)
    
    img = np.array(img_pil)
    
    if img.ndim == 3 and img.shape[2] == 4:
        alpha = img[:, :, 3]
        gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        gray[alpha == 0] = 255
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if img.ndim == 3 else img
        
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    cv2.imwrite(output_path, enhanced)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <path_to_photo>")
    else:
        prep_photo(sys.argv[1])
