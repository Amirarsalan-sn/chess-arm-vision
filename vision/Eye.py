from ultralytics import YOLO
import numpy as np
import cv2


class Eye:
    def __init__(self, color):
        self.model_pieces = YOLO('yolo11n_best_hand_made.pt')
        self.model_points = YOLO('yolo11n_best_points.pt')
        self.color = color
        self.desired_width = 1920  # Change this to your desired width
        self.desired_height = 1080  # Change this to your desired height
        self.mask_to_piece = {0: 'B',
                              1: 'K',
                              2: 'N',
                              3: 'P',
                              4: 'Q',
                              5: 'R',
                              6: 'b',
                              7: 'k',
                              8: 'n',
                              9: 'p',
                              10: 'q',
                              11: 'r'}

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.desired_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.desired_height)

        if not self.cap:
            raise Exception("Error: Could not open webcam.")

        self.rgb_lower_bound = np.array([20, 30, 118])
        self.rgb_upper_bound = np.array([70, 75, 210])

    # TODO: Implement it.

    def extract_points_with_yolo(self, image):
        image_resized = cv2.resize(image, (1280, 1280))
        results = self.model_points.predict(source=image_resized)[0].boxes

        x_list = []
        y_list = []
        coordinates = []
        for result in results:
            coordinates.append([result.xyhw[0], result.xyhw[1]])
            x_list.append(result.xyhw[0])
            y_list.append(result.xyhw[1])

        if len(coordinates) != 4:
            raise Exception("the yolo model couldn't find the four red corners.")

        x_list.sort()
        y_list.sort()

        try:
            median_x = (x_list[1] + x_list[2]) / 2
            median_y = (y_list[1] + y_list[2]) / 2
        except Exception as e:
            raise Exception("fatal points, not enough points where recognized.")

        print(f'sum x :{median_x}, sum y: {median_y}')
        tl = bl = tr = br = None
        for pos in coordinates:
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
            raise Exception('fatal, could not specify tl, bl, tr, br.')

        return tl, bl, tr, br

    def extract_points_with_hsv(self, image):
        mask = cv2.inRange(image, self.rgb_lower_bound, self.rgb_upper_bound)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours and print coordinates
        perspect_list = []
        x_list = []
        y_list = []
        for contour in contours:
            # Get the coordinates of the bounding box
            x, y, w, h = cv2.boundingRect(contour)
            if 5 <= w <= 16 and 5 <= h <= 16:
                print(f"Top-left corner: ({x}, {y}) , width: ({w}, {h})")
                # Draw a rectangle around the detected point
                perspect_list.append([x + (w // 2), y + (h // 2)])
                x_list.append(x + (w // 2))
                y_list.append(y + (h // 2))

        if len(perspect_list) != 4:
            raise Exception("the hsv model couldn't find the four red corners.")

        x_list.sort()
        y_list.sort()

        try:
            median_x = (x_list[1] + x_list[2]) / 2
            median_y = (y_list[1] + y_list[2]) / 2
        except Exception as e:
            raise Exception("fatal points, not enough points where recognized.")

        print(f'sum x :{median_x}, sum y: {median_y}')
        tl = bl = tr = br = None
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
            raise Exception('fatal, could not specify tl, bl, tr, br.')

        return tl, bl, tr, br

    def look(self):
        """
        takes a screenshot from the board and extracts its four corners and applies perspective transformation on it
        then gives it to YOLO to detect the chess pieces. Finally, finds the location of each chess piece in the board.
        :return: A 8x8 matrix showing the current state of the chess board. Indicating the exact piece that is present
        in each tile of the board.
        """

        result_map = [[[''] for j in range(8)] for i in range(8)]

        # Capture a single frame
        ret, img = self.cap.read()

        tl, bl, tr, br = self.extract_points_with_yolo(img)

        pts1 = np.float32([tr, tl, br, bl])

        # Coordinates of the square in the transformed image
        # Transforming it to a rectangle of size 640x640
        pts2 = np.float32([[0, 0], [0, 640], [640, 0], [640, 640]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        # Perform the perspective transformation
        transformed_frame = cv2.warpPerspective(img, M, (640, 640))

        result = self.model_pieces(source=transformed_frame)[0].boxes

        for box in result:
            piece = self.mask_to_piece[int(box.cls.item())]
            if self.color == 1:
                pos_y = box.xywh[0] // 80
                pos_x = box.xwyh[1] // 80
            else:
                pos_y = 7 - (box.xywh[0] // 80)
                pos_x = 7 - (box.xwyh[1] // 80)
            result_map[pos_x][pos_y] = piece

            label = f"{piece}: {box.conf.item():2.f}"

            cv2.rectangle(transformed_frame, (int(box.xyxy[0]), int(box.xyxy[1])), (int(box.xyxy[2]), int(box.xyxy[3])),
                          (0, 255, 0), 2)
            cv2.putText(transformed_frame, label, (int(box.xyxy[0]), int(box.xyxy[1] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('Detected Pieces', transformed_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return result_map
