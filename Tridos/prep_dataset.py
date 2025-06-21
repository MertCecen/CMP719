import os
import cv2
import numpy as np

# Define paths
base_path = "SIRST-5K"
image_dir = os.path.join(base_path, "images").replace("\\","/")
mask_dir = os.path.join(base_path, "masks").replace("\\","/")
output_txt = os.path.join(base_path, "annotations.txt").replace("\\","/")

os.makedirs(os.path.dirname(output_txt), exist_ok=True)

with open(output_txt, 'w') as f_out:
    for filename in sorted(os.listdir(image_dir)):
        if not filename.endswith(".png"):
            continue

        image_path = os.path.join(image_dir, filename).replace("\\","/")
        mask_path = os.path.join(mask_dir, filename).replace("\\","/")

        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            continue

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            continue

        line = image_path
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            x1, y1, x2, y2 = x, y, x + w, y + h
            line += f" {x1},{y1},{x2},{y2},0"

        f_out.write(line + "\n")
