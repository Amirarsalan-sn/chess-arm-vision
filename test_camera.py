import cv2
import numpy as np

cap = cv2.VideoCapture(0)

desired_width = 1920  # Change this to your desired width
desired_height = 1080  # Change this to your desired height

# Set the width and height for the webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Check if the webcam is opened correctly
if not cap:
    print("Error: Could not open webcam.")
else:
    # Capture a single frame
    ret, img = cap.read()
    print(img.shape)
    #img = cv2.imread('test_image_2.jpg')
    resized = cv2.resize(img, (800, 600))
    cv2.imshow("captured", resized)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Convert the image to HSV color space

    # Define the range for bright red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours and print coordinates
    perspect_list = []
    sum_x = 0
    sum_y = 0
    for contour in contours:
        # Get the coordinates of the bounding box
        x, y, w, h = cv2.boundingRect(contour)
        if 5 <= w <= 30 and 5 <= h <= 30:
            print(f"Top-left corner: ({x}, {y}) , width: ({w}, {h})")
            # Draw a rectangle around the detected point
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            perspect_list.append([x+(w//2), y+(h//2)])
            sum_x += x + (w//2)
            sum_y += y + (h//2)

    sum_x /= 4
    sum_y /= 4

    tl = bl = tr = br = None
    for pos in perspect_list:
        if pos[0] < sum_x and pos[1] < sum_y:
            tl = pos
        elif pos[0] < sum_x and pos[1] > sum_y:
            bl = pos
        elif pos[0] > sum_x and pos[1] < sum_y:
            tr = pos
        elif pos[0] > sum_x and pos[1] > sum_y:
            br = pos

    print(f'tl:{tl}, bl:{bl}, tr:{tr}, br:{br}')

    pts1 = np.float32([tl, bl, tr, br])

    # Coordinates of the square in the transformed image
    # Transforming it to a rectangle of size 640x640
    pts2 = np.float32([[0, 0], [0, 640], [640, 0], [640, 640]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    # Perform the perspective transformation
    transformed_frame = cv2.warpPerspective(img, M, (640, 640))

    # Display the result
    cv2.imshow('Detected Points', cv2.resize(img, (800, 600)))
    cv2.imshow('transformed', transformed_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


