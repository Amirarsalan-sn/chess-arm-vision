import math

import cv2
import numpy as np

tl = [406, 483]
bl = [742, 927]
tr = [838, 190]
br = [1192, 529]

cap = cv2.VideoCapture(0)

desired_width = 1920  # Change this to your desired width
desired_height = 1080  # Change this to your desired height

# Set the width and height for the webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)


def fix_camera():
    global cap, tl, tr, bl, br
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            break

        # Draw contours on the original frame in green
        cv2.rectangle(frame, (tl[0] - 5, tl[1] - 5), (tl[0] + 5, tl[1] + 5), (0, 255, 0), 2)
        cv2.rectangle(frame, (bl[0] - 5, bl[1] - 5), (bl[0] + 5, bl[1] + 5), (0, 255, 0), 2)
        cv2.rectangle(frame, (tr[0] - 5, tr[1] - 5), (tr[0] + 5, tr[1] + 5), (0, 255, 0), 2)
        cv2.rectangle(frame, (br[0] - 5, br[1] - 5), (br[0] + 5, br[1] + 5), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video Feed', cv2.resize(frame, (800, 600)))

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def find_contours():
    global cap
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        img_2 = frame.copy()
        if not ret:
            break

        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Convert the image to HSV color space

        # Define the lower and upper bounds for red color in HSV
        lower_red = np.array([20, 30, 120])
        upper_red = np.array([70, 75, 210])

        # Create a mask for the red color
        mask = cv2.inRange(frame, lower_red, upper_red)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours and print coordinates
        perspect_list = []
        sum_x = 0
        sum_y = 0
        # tl = bl = tr = br = None
        for contour in contours:
            # Get the coordinates of the bounding box
            x, y, w, h = cv2.boundingRect(contour)
            if 5 <= w <= 30 and 5 <= h <= 30:
                print(f"Top-left corner: ({x}, {y}) , width: ({w}, {h})")
                # Draw a rectangle around the detected point
                cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                perspect_list.append([x + (w // 2), y + (h // 2)])

        cv2.imshow('Video Feed', cv2.resize(img_2, (800, 600)))

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


image = None


def get_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the pixel value at (x, y)
        pixel = image[y, x]
        # Convert the pixel from BGR to HSV
        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
        # Print the HSV value
        print(f"RGB: {pixel}, HSV: {hsv_pixel[0][0]}")


def find_hsv():
    global cap, image
    # Capture a single frame
    ret, image = cap.read()

    if ret:
        # Resize for consistency
        image = cv2.resize(image, (800, 600))

        # Display the image
        cv2.imshow('Image', image)

        # Set the mouse callback function
        cv2.setMouseCallback('Image', get_hsv)

        # Wait until a key is pressed
        cv2.waitKey(0)


# Check if the webcam is opened correctly
if not cap:
    print("Error: Could not open webcam.")
else:
    """find_contours()
    exit(0)"""
    i = 0
    while (True):

        tr = br = bl = tl = None
        ret, img = cap.read()
        img_2 = img.copy()
        print(img.shape)
        # img = cv2.imread('test_image_2.jpg')
        resized = cv2.resize(img, (800, 600))
        # cv2.imshow("captured", resized)

        # Define the range for bright red color in HSV
        lower_red = np.array([20, 30, 118])
        upper_red = np.array([70, 75, 210])

        # Create a mask for the red color
        mask = cv2.inRange(img, lower_red, upper_red)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours and print coordinates
        perspect_list = []
        x_list = []
        y_list = []
        tl = bl = tr = br = None
        for contour in contours:
            # Get the coordinates of the bounding box
            x, y, w, h = cv2.boundingRect(contour)
            if 5 <= w <= 16 and 5 <= h <= 16:
                print(f"Top-left corner: ({x}, {y}) , width: ({w}, {h})")
                # Draw a rectangle around the detected point
                cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                perspect_list.append([x + (w // 2), y + (h // 2)])
                x_list.append(x + (w // 2))
                y_list.append(y + (h // 2))

        x_list.sort()
        y_list.sort()

        try:
            median_x = (x_list[1] + x_list[2])/2
            median_y = (y_list[1] + y_list[2])/2
        except Exception as e:
            print("fatal points")
            continue

        print(f'sum x :{median_x}, sum y: {median_y}')
        # tl = bl = tr = br = None
        for pos in perspect_list:
            if pos[0] < median_x and pos[1] < median_y:
                tl = pos
            elif pos[0] < median_x and pos[1] > median_y:
                bl = pos
            elif pos[0] > median_x and pos[1] < median_y:
                tr = pos
            elif pos[0] > median_x and pos[1] > median_y:
                br = pos

        print(f'tl:{tl}, bl:{bl}, tr:{tr}, br:{br}')

        if tl is None or bl is None or tr is None or br is None:
            print('fatal')
            continue

        pts1 = np.float32([tr, tl, br, bl])

        # Coordinates of the square in the transformed image
        # Transforming it to a rectangle of size 640x640
        pts2 = np.float32([[0, 0], [0, 640], [640, 0], [640, 640]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        # Perform the perspective transformation
        transformed_frame = cv2.warpPerspective(img, M, (640, 640))

        # Display the result
        cv2.imshow('Detected Points', cv2.resize(img_2, (800, 600)))
        cv2.imshow('transformed', transformed_frame)
        key = cv2.waitKey(0)
        if key == ord('y'):  # Save the image if 'y' is pressed
            cv2.destroyAllWindows()
            cv2.imwrite(f'data_set/{i}.jpg', transformed_frame)
            cv2.imwrite(f'data_set/original/{i}.jpg', img)
            i += 1
            print(f"saved. file {i}")
        elif key == ord('n'):  # Take another image if 'n' is pressed
            cv2.destroyAllWindows()
            continue
        elif key == ord('q'):  # Quit if 'q' is pressed
            break


