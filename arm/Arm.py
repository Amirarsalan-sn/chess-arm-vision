from MG400.dobot_api import DobotApiDashboard, DobotApiMove, DobotApi


class Arm:
    def __init__(self, color):
        try:
            ip = "192.168.1.6"
            dashboard_p = 29999
            move_p = 30003
            feed_p = 30004
            print("Establishing connection ...")
            self.dashboard = DobotApiDashboard(ip, dashboard_p)
            self.move = DobotApiMove(ip, move_p)
            self.feed = DobotApi(ip, feed_p)
            print(">.<Connection Successful>!<")
        except Exception as e:
            print(":(Connection Failed:(")
            raise e

        self.color = color
        self.rotation = 34.6
        self.board_position_encoding = [
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]],
            [[None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation], [None, None, None, self.rotation],
             [None, None, None, self.rotation], [None, None, None, self.rotation]], ]

        self.void_pos = [None, None, None, self.rotation]  # used for captures and promotions
        self.promotion_poses = {
            'q': [None, None, None, self.rotation],
            'b': [None, None, None, self.rotation],
            'r': [None, None, None, self.rotation],
            'kn': [None, None, None, self.rotation]
        }

        self.word_to_pos = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        self.time_to_wait = 200

    # TODO: to be implemented
    def move(self, action: str, capture: bool):
        """
        This method takes a chess action (in uci format) and performs it using the robotic arm.
        Note that there are multiple types of actions and each needs different sequences of actions to be performed by
        the robot:
        Simple move,
        Simple move with capture,
        Promotion,
        Promotion with capture,
        Castling
        :param capture: a boolean indicating whether to perform capture action or not.
        :param action: chess action (in uci format)
        :return: nothing
        """
        pass

    def simple_move(self, action: str, capture: bool):
        pass

    def promotion(self, action: str, capture: bool):
        pass

    def castling(self, action: str):
        pass

    def act(self, start_pos, end_pos):
        """
        Performs an actual robot action. moves a chess piece from a starting position to an ending position.
        :param start_pos: starting position
        :param end_pos: ending position
        :return: nothing
        """
        delta = 20
        start_pos_delta = [start_pos[0], start_pos[1], start_pos[2] + delta, start_pos[3]]
        end_pos_delta = [end_pos[0], end_pos[1], end_pos[2] + delta, end_pos[3]]

        self.dashboard.EnableRobot()  # No parameters
        self.reset_pos()
        self.dashboard.SetPayload(0.5)
        self.move.MovL(*start_pos)
        # input('proceed ? :')
        self.dashboard.wait(self.time_to_wait)
        self.dashboard.DO(1, 1)
        # input('proceed ? :')
        self.dashboard.wait(self.time_to_wait)
        # input('proceed ? :')
        self.move.MovL(*start_pos_delta)
        self.move.MovL(*end_pos_delta)
        self.move.MovL(*end_pos)
        # input('proceed ? :')
        self.dashboard.wait(self.time_to_wait)
        self.dashboard.DO(1, 0)
        self.dashboard.wait(self.time_to_wait)
        self.reset_pos()

        self.dashboard.SetPayload(0)

        self.dashboard.DisableRobot()

    def reset_pos(self):
        """
        The starting position of the robot.
        :return: nothing
        """
        pass

    def close_connection(self):
        self.dashboard.close()
        self.move.close()
        self.feed.close()
