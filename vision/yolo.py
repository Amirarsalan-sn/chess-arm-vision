import os
import random
import shutil
from ultralytics import YOLO

train = False


def move_random_files(src_images_dir, src_labels_dir, dest_images_dir, dest_labels_dir, num_files=6000):
    # Get list of all image files in the source images directory
    image_files = [f for f in os.listdir(src_images_dir) if f.endswith('.jpg')]

    # Randomly select the specified number of image files
    selected_files = random.sample(image_files, num_files)

    # Move the selected image files and their corresponding label files
    for file_name in selected_files:
        # Move image file
        src_image_path = os.path.join(src_images_dir, file_name)
        dest_image_path = os.path.join(dest_images_dir, file_name)
        shutil.move(src_image_path, dest_image_path)

        # Move corresponding label file
        label_file_name = os.path.splitext(file_name)[0] + '.txt'
        src_label_path = os.path.join(src_labels_dir, label_file_name)
        dest_label_path = os.path.join(dest_labels_dir, label_file_name)
        if os.path.exists(src_label_path):
            shutil.move(src_label_path, dest_label_path)


src_images_dir = './train/images'
src_labels_dir = './train/labels'
dest_images_dir = './val/images'
dest_labels_dir = './val/labels'

if train:
    """move_random_files(src_images_dir, src_labels_dir, dest_images_dir, dest_labels_dir)
    print(f"data split done")
    exit(0)"""
    model = YOLO("yolo11n.pt")

    model.train(data="data.yaml", device=0, epochs=10, imgsz=640, batch=8, workers=0)

else:
    model = YOLO("yolo11n_best.pt")

    model.predict(source='clean_board.jpg', show=True, save=True)
