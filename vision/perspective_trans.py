import cv2
import numpy as np


def get_pixel_location(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: ({x}, {y})")


# Coordinates of the square in the original image
pts1 = np.float32([[326, 50], [275, 651], [924, 48], [986, 651]])

# Coordinates of the square in the transformed image
# Transforming it to a rectangle of size 640x640
pts2 = np.float32([[0, 0], [640, 0], [0, 640], [640, 640]])

# Load the video
video = cv2.VideoCapture('test.mp4')

# Define the codec and create VideoWriter object
out = cv2.VideoWriter('transformed_video_640x640_reversed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 640))

while True:
    ret, frame = video.read()
    if not ret:
        break
    # Get the perspective transformation matrix
    M = cv2.getPerspectiveTransform(pts1, pts2)

    # Perform the perspective transformation
    transformed_frame = cv2.warpPerspective(frame, M, (640, 640))

    # Write the transformed frame to the output video
    #out.write(transformed_frame)
    cv2.imshow('Frame', frame)
    #cv2.setMouseCallback('Frame', get_pixel_location)
    cv2.imshow('Frame_transform', transformed_frame)
    if cv2.waitKey(1) == 27:
        break

    out.write(transformed_frame)
# Release everything if job is finished
#video.release()
#out.release()

print("Perspective transformation completed and saved as 'transformed_video_640x640.mp4'.")