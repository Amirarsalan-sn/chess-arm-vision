from MG400.dobot_api import DobotApiDashboard, DobotApiMove, DobotApi
import re


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
    def move(self, action: str, capture: bool, castling: bool):
        """
        This method takes a chess action (in uci format) and performs it using the robotic arm.
        Note that there are multiple types of actions and each needs different sequences of actions to be performed by
        the robot:
        Simple move,
        Simple move with capture,
        Promotion,
        Promotion with capture,
        Castling
        :param castling: a boolean indicating whether to perform castling action or not.
        :param capture: a boolean indicating whether to perform capture action or not.
        :param action: chess action (in uci format)
        :return: nothing
        """

        if castling:
            self.castling(action)
        elif len(action) > 4:
            self.promotion(action, capture)
        else:
            self.simple_move(action, capture)

    def simple_move(self, action: str, capture: bool):
        end_pos, start_pos = self.extract_pos(action)
        if capture:
            self.act(end_pos, self.void_pos)

        self.act(start_pos, end_pos)
        self.reset_pos()

    def promotion(self, action: str, capture: bool):
        end_pos, start_pos = self.extract_pos(action)
        if capture:
            self.act(end_pos, self.void_pos)

        self.act(start_pos, self.void_pos)
        self.act(self.promotion_poses[action[-1]], end_pos)
        self.reset_pos()

    def extract_pos(self, action):
        start_action = action[0:2]
        end_action = action[2:4]
        start_pos = [int(start_action[1]) - 1 if self.color == 1 else -1 * int(start_action[1]),
                     self.word_to_pos[start_action[0]] if self.color == 1 else -1 * self.word_to_pos[start_action[0]]-1]
        end_pos = [int(end_action[1]) - 1 if self.color == 1 else int(end_action[1]) - 8,
                   self.word_to_pos[end_action[0]] if self.color == 1 else -1 * self.word_to_pos[end_action[0]] - 1]
        return end_pos, start_pos

    def castling(self, action: str):
        start_pos, end_pos = self.extract_pos(action)

        self.act(start_pos, end_pos)

        if int(action[1]) < int(action[3]):  # king side castling.
            second_start_action = f'{action[0]}7'
            second_end_action = f'{action[2]}5'
        elif int(action[1]) > int(action[3]):  # queen side castling.
            second_start_action = f'{action[0]}0'
            second_end_action = f'{action[2]}3'

        second_action = second_start_action + second_end_action
        second_start_pos, second_end_pos = self.extract_pos(second_action)
        self.act(second_start_pos, second_end_pos)
        self.reset_pos()

    def act(self, start_pos, end_pos):
        """
        Performs an actual robot action. moves a chess piece from a starting position to an ending position.
        :param start_pos: starting position
        :param end_pos: ending position
        :return: nothing
        """
        delta = 3.5
        start_pos_delta = [start_pos[0], start_pos[1], start_pos[2] + delta, start_pos[3]]
        end_pos_delta = [end_pos[0], end_pos[1], end_pos[2] + delta, end_pos[3]]

        self.dashboard.EnableRobot()  # No parameters
        self.reset_pos()
        self.dashboard.SetPayload(0.5)
        self.move.MovL(*start_pos_delta)
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
        self.move.MovL(*end_pos_delta)

        self.dashboard.SetPayload(0)

        self.dashboard.DisableRobot()

    def reset_pos(self):
        """
        The starting position of the robot.
        :return: nothing
        """
        pass

    def memories(self):
        poses = [[[] for j in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                input("proceed? ")
                pos = self.dashboard.GetPose()
                pos = re.findall("[-+]?\d*\.\d+,\s*[-+]?\d*\.\d+,\s*[-+]?\d*\.\d+,\s*[-+]?\d*\.\d+", pos)[0]
                pos = pos.split(',')
                poses[i][j] = [float(pos[0]), float(pos[1]), float(pos[2])]

        print(f'Memorised positions:\n{poses}')

    def close_connection(self):
        self.dashboard.close()
        self.move.close()
        self.feed.close()
