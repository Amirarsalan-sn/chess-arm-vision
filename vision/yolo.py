import os
import random
import shutil
from ultralytics import YOLO

train = False

if train:
    model = YOLO("yolo11n.pt")

    model.train(data="data.yaml", device=0, epochs=10, imgsz=640, batch=8, workers=0)

else:
    model = YOLO("yolo11n_best.pt")

    model.predict(source='clean_board.jpg', show=True, save=True)
