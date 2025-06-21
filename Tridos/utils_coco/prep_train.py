import os
import ast
image_dir = "../IRDST_real/images/train.txt"
box_dir = "../IRDST_real/boxes/train.txt"

out_img_dir = "IRDST_real/images/train.txt"
out_box_dir = "IRDST_real/boxes/train.txt"
output_txt = "irstd_train.txt"

image_files = sorted(os.listdir(image_dir))

with open(output_txt, "w") as out_file:
    for img_file in image_files:
        if not img_file.endswith(".png"):
            continue

        #out_img_file = str(int(img_file.replace(".png",""))) + ".png"
        image_path = os.path.join(out_img_dir, img_file).replace("\\", "/")

        box_file = os.path.join(box_dir, img_file.replace(".png", ".txt"))

        if not os.path.exists(box_file):
            continue

        out_file.write(image_path)

        with open(box_file, "r") as bf:
            for line in bf:
                line = line.strip()
                if not line:
                    continue  # skip empty lines

                try:
                    if line.startswith("["):
                        # Handle list-like format: [x, y, w, h]
                        parts = line.strip("[]").split(",")
                    else:
                        # Handle space-separated format: x y w h
                        parts = line.split()

                    if len(parts) < 4:
                        continue  # skip invalid lines

                    x, y, w, h = map(int, parts[:4])
                    x2 = x + w
                    y2 = y + h
                    out_file.write(f" {x},{y},{x2},{y2},0")
                except Exception as e:
                    print(f"Error parsing {box_file}: {line} ({e})")
                    continue

        out_file.write("\n")
