from ultralytics import YOLO


class Eye:
    def __init__(self, color):
        self.model = YOLO('yolo11n_best.pt')
        self.color = color

    # TODO: Implement it.
    def look(self):
        """
        takes a screenshot from the board and extracts its four corners and applies perspective transformation on it
        then gives it to YOLO to detect the chess pieces. Finally, finds the location of each chess piece in the board.
        :return: A 8x8 matrix showing the current state of the chess board. Indicating the exact piece that is present
        in each tile of the board.
        """
        pass
