import time

from ultralytics import YOLO
import numpy as np
import cv2


class Eye:
    def __init__(self, color):
        self.model_pieces = YOLO('D:/chess_arm_vision/vision/yolo11n_best_hand_made.pt')
        self.model_points = YOLO('D:/chess_arm_vision/vision/yolo11n_best_points.pt')
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

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.desired_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.desired_height)

        if not self.cap:
            raise Exception("Error: Could not open webcam.")

        self.rgb_lower_bound = np.array([20, 30, 118])
        self.rgb_upper_bound = np.array([70, 75, 210])

        self.tl = None
        self.tr = None
        self.bl = None
        self.br = None

        self.corner_points = []

        img = self.read_image()
        self.extract_points_with_roll_back(img)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

    # TODO: Implement it.

    def read_image(self):
        try:
            self.cap.read()
            ret, img = self.cap.read()
            if not ret:
                print('could not read frame so trying to recapture the webcam.')
                self.recapture()
                self.cap.read()
                ret, img = self.cap.read()
                if not ret:
                    raise Exception('could not read frame ret value is None')
        except Exception as e:
            raise Exception(f'Encountered an exception while capturing image from webcam: {e}\n')

        return img

    def extract_points_with_yolo(self, image):
        image_resized = cv2.resize(image, (1280, 1280))
        results = self.model_points.predict(source=image_resized)[0].boxes
        scale_width = 1920 / 1280
        scale_hight = 1080 / 1280

        x_list = []
        y_list = []
        coordinates = []
        for i in range(results.cls.shape[0]):
            x = int(results.xywh[i][0] * scale_width)
            y = int(results.xywh[i][1] * scale_hight)
            cv2.rectangle(image_resized, (int(results.xyxy[i][0]), int(results.xyxy[i][1])),
                          (int(results.xyxy[i][2]), int(results.xyxy[i][3])), (0, 255, 0), 2)
            coordinates.append([x, y])
            x_list.append(x)
            y_list.append(y)

        cv2.imshow('Detected points', cv2.resize(image_resized, (640, 640)))

        if len(coordinates) != 4 and self.tl is None:
            raise Exception("the yolo model couldn't find the four red corners.")
        elif len(coordinates) != 4:
            print('using previously saved points')
            tl = self.tl
            tr = self.tr
            bl = self.bl
            br = self.br
            print(f'tl:{tl}, bl:{bl}, tr:{tr}, br:{br}')

            return tl, bl, tr, br

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

        if (tl is None or bl is None or tr is None or br is None) and (self.tl is None):
            raise Exception('fatal, could not specify tl, bl, tr, br.')
        elif tl is None or bl is None or tr is None or br is None:
            print('using previously saved points')
            tl = self.tl
            tr = self.tr
            bl = self.bl
            br = self.br
        else:
            print('red corner positions saved.')
            self.tl = tl
            self.tr = tr
            self.bl = bl
            self.br = br

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

    def capture_points(self, event, x, y, flags, param):
        """Capture mouse clicks for point selection."""
        if event == cv2.EVENT_LBUTTONDOWN and len(self.corner_points) < 4:
            self.corner_points.append([x, y])

    def insert_manually(self):
        self.corner_points.clear()
        point_names = ['Top Left', 'Bottom Left', 'Top Right', 'Bottom Right']
        cv2.namedWindow("Webcam Feed")
        cv2.setMouseCallback("Webcam Feed", self.capture_points)

        while len(self.corner_points) < 4:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Resize frame for display
            display_frame = cv2.resize(frame, (600, 400))

            # Show instructions
            if len(self.corner_points) < 4:
                cv2.putText(display_frame, f"Click on {point_names[len(self.corner_points)]}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Draw points if available
            for pt in self.corner_points:
                cv2.circle(display_frame, pt, 5, (0, 255, 0), -1)

            cv2.imshow("Webcam Feed", display_frame)

            cv2.waitKey(20)

        original_points = [[int(pt[0] * (1920 / 600)), int(pt[1] * (1080 / 400))] for pt in self.corner_points]

        self.tl = original_points[0]
        self.bl = original_points[1]
        self.tr = original_points[2]
        self.br = original_points[3]
        cv2.destroyAllWindows()

        print(f'manually set points: tl: {self.tl}, bl: {self.bl}, tr: {self.tr}, br: {self.br}')

        return self.tl, self.bl, self.tr, self.br

    def extract_points_with_roll_back(self, img):
        flag = False

        tl = bl = tr = br = None

        for i in range(10):
            try:
                tl, bl, tr, br = self.extract_points_with_yolo(img)
                flag = True
                break
            except Exception as e:
                print(f'Attempt {i} failed for finding red corners.')
                continue

        if not flag:
            command = input('Could not find 4 points, do you want to insert them manually (Y/n) ??')
            if command == '' or command == 'Y' or command == 'y':
                tl, bl, tr, br = self.insert_manually()
            else:
                raise Exception("the yolo model couldn't find the four red corners.")

        return tl, bl, tr, br

    def look(self):
        """
        takes a screenshot from the board and extracts its four corners and applies perspective transformation on it
        then gives it to YOLO to detect the chess pieces. Finally, finds the location of each chess piece in the board.
        :return: A 8x8 matrix showing the current state of the chess board. Indicating the exact piece that is present
        in each tile of the board.
        """
        while True:
            result_map = [['' for j in range(8)] for i in range(8)]

            # Capture a single frame
            img = self.read_image()

            tl, bl, tr, br = self.extract_points_with_roll_back(img)

            pts1 = np.float32([tr, tl, br, bl])

            # Coordinates of the square in the transformed image
            # Transforming it to a rectangle of size 640x640
            pts2 = np.float32([[0, 0], [0, 640], [640, 0], [640, 640]])

            M = cv2.getPerspectiveTransform(pts1, pts2)

            # Perform the perspective transformation
            transformed_frame = cv2.warpPerspective(img, M, (640, 640))

            result = self.model_pieces(source=transformed_frame)[0].boxes

            for i in range(result.cls.shape[0]):
                piece = self.mask_to_piece[int(result.cls[i].item())]
                """if result.conf[i].item() < 0.50:
                    continue"""
                if self.color == 1:
                    pos_y = int(result.xywh[i][0].item() // 80)
                    pos_x = int(7 - result.xywh[i][1].item() // 80)
                else:
                    pos_y = int(7 - result.xywh[i][0].item() // 80)
                    pos_x = int(result.xywh[i][1].item() // 80)

                if (result_map[pos_x][pos_y] == '') or (result_map[pos_x][pos_y] == 'K' and piece == 'k'):
                    result_map[pos_x][pos_y] = piece
                else:
                    continue

                label = f"{piece}: {result.conf[i].item():.2f}"

                cv2.rectangle(transformed_frame, (int(result.xyxy[i][0]), int(result.xyxy[i][1])),
                              (int(result.xyxy[i][2]), int(result.xyxy[i][3])), (0, 255, 0), 2)
                cv2.putText(transformed_frame, label, (int(result.xyxy[i][0]), int(result.xyxy[i][1] + 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow('Detected Pieces', transformed_frame)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
            """command = input('accept (Y/n)? ')
            if command == 'Y' or command == '':
                break
            else:
                continue"""
            break
        return result_map

    def close(self):
        self.cap.release()
        print('webcam released.')

    def recapture(self):
        self.cap.release()
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.desired_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.desired_height)


if __name__ == '__main__':
    eye = Eye(1)
    while True:
        comm = input('continue? ')
        if not (comm == '' or comm == 'Y'):
            eye.close()
            break
        eye.look()
