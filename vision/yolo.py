from ultralytics import YOLO

train = True

if train:
    model = YOLO("yolo11n.pt")

    model.train(data="data_points.yaml", device=0, epochs=10, imgsz=1280, batch=8, workers=0)

else:
    model = YOLO("yolo11n_best_hand_made.pt")

    model.predict(source='../data_set/0.jpg', show=True, save=True)
    model.predict(source='../data_set/1.jpg', show=True, save=True)
    model.predict(source='../data_set/2.jpg', show=True, save=True)


