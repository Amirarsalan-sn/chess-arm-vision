from ultralytics import YOLO
import numpy as np
import cv2


class Eye:
    def __init__(self, color):
        self.model = YOLO('yolo11n_best.pt')
        self.color = color
        self.desired_width = 1920  # Change this to your desired width
        self.desired_height = 1080  # Change this to your desired height
        self.mask_to_piece = {0: 'K',
                              1: 'k',
                              2: 'Q',
                              3: 'q',
                              4: 'B',
                              5: 'b',
                              6: 'N',
                              7: 'n',
                              8: 'R',
                              9: 'r',
                              10: 'P',
                              11: 'p'}

    # TODO: Implement it.
    def look(self):
        """
        takes a screenshot from the board and extracts its four corners and applies perspective transformation on it
        then gives it to YOLO to detect the chess pieces. Finally, finds the location of each chess piece in the board.
        :return: A 8x8 matrix showing the current state of the chess board. Indicating the exact piece that is present
        in each tile of the board.
        """
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.desired_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.desired_height)

        result_map = [[[''] for j in range(8)] for i in range(8)]

        if not cap:
            raise Exception("Error: Could not open webcam.")
        else:
            # Capture a single frame
            ret, img = cap.read()
            # img = cv2.imread('test_image_2.jpg')
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
                    perspect_list.append([x + (w // 2), y + (h // 2)])
                    sum_x += x + (w // 2)
                    sum_y += y + (h // 2)

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

            result = self.model(source=transformed_frame)[0]

            for (box, cls) in zip(result.boxes.xywh, result.cls):
                piece = self.mask_to_piece[cls]
                bl = [box[0], box[1] + box[3]]
                pos_y = bl[0] // 80
                pos_x = bl[1] // 80
                result_map[pos_x][pos_y] = piece

            # Display the result
            """cv2.imshow('Detected Points', cv2.resize(img, (800, 600)))
            cv2.imshow('transformed', transformed_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()"""

        return result_map
