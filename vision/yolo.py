from ultralytics import YOLO

train = False

if train:
    model = YOLO("yolo11n.pt")

    model.train(data="data.yaml", device=0, epochs=8, imgsz=640, batch=8, workers=0)

else:
    model = YOLO("yolo11n_best_hand_made.pt")

    """model.predict(source='./val/images/463_jpg.rf.8699768a8193469473b2a09afdc8a6d7_mirrored_left.jpg', show=True, save=True)
    model.predict(source='./val/images/469_jpg.rf.758d0b1bf71b41555f796028b537b19b.jpg', show=True, save=True)
    model.predict(source='./val/images/470_jpg.rf.07fbf0ab0728c4b9fd56b90a87268b7b_mirrored_up.jpg', show=True, save=True)
    model.predict(source='./val/images/473_jpg.rf.0e4908833c1ee2a8bc561c16470945f9.jpg', show=True, save=True)
    model.predict(source='./val/images/475_jpg.rf.2297fb19347cc4e9578bcdad0121238e_mirrored_left.jpg', show=True, save=True)
    model.predict(source='./val/images/477_jpg.rf.e82e154ff89fded7adc607bbdf58ca5d.jpg', show=True, save=True)"""
    result = model.predict(source='./val/images/483_jpg.rf.4d01e54cfb318ec7e31af67bc80de9eb_mirrored_right.jpg', show=True, save=False)
    for box in result.boxes:
        print(box)
