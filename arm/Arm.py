from arm.MG400.dobot_api import DobotApiDashboard, DobotApiMove, DobotApi
import re
import matplotlib.pyplot as plt

memor = [
    [[219.367455, 90.64524, -101.370293], [217.368459, 64.153626, -100.919762], [219.160661, 34.708657, -100.980217],
     [218.968025, 10.887078, -101.830238], [216.286527, -18.791501, -102.89], [215.447061, -46.231246, -102.059448],
     [214.332562, -73.240207, -103.407181], [213.578113, -100.045619, -104.496399]],
    [[245.784483, 90.438647, -99.247955], [245.624762, 62.120484, -99.488686], [244.968324, 33.925449, -100.709206],
     [243.070623, 7.733113, -100.826385], [242.503628, -18.392415, -100.82798], [242.464164, -45.84832, -101.756836],
     [240.920087, -75.332494, -102.249306], [239.294877, -102.370251, -102.682846]],
    [[273.172697, 90.768907, -98.224518], [273.281607, 61.992447, -98.826538], [272.307634, 36.505854, -98.877731],
     [269.909316, 5.15435, -99.905304], [269.32602, -18.403682, -99.906784], [269.653027, -47.434009, -100.38739],
     [267.788598, -75.716347, -101.556595], [266.883009, -101.489618, -101.297798]],
    [[302.352395, 88.30897, -98.291679], [299.51014, 61.530741, -97.957573], [299.242875, 35.374911, -98.764526],
     [297.922649, 6.763841, -99.022255], [297.352871, -19.573545, -99.022797], [295.145612, -46.907967, -99.844543],
     [294.914439, -74.966783, -100.213394], [294.064012, -100.604206, -101.15966]],
    [[327.281366, 87.710211, -97.893082], [326.4294, 60.27098, -98.47702], [325.933452, 33.484379, -98.465942],
     [325.355283, 5.09296, -98.923325], [324.712448, -20.990638, -98.925873], [321.695438, -48.899527, -98.925613],
     [321.052005, -74.745984, -99.314484], [319.953111, -101.566207, -100.942352]],
    [[354.646977, 86.675485, -98.057198], [354.12078, 57.729036, -97.657852], [352.338718, 31.058388, -98.283897],
     [352.426214, 5.951999, -98.019691], [350.504418, -21.062961, -98.36747], [347.838388, -48.000604, -98.369499],
     [348.267652, -75.315152, -98.641106], [348.005624, -102.97829, -100.29171]],
    [[381.934834, 87.504829, -97.563469], [380.14346, 58.341452, -97.502022], [379.860583, 32.58821, -99.24],
     [378.057758, 4.67567, -97.166656], [377.457868, -21.784855, -97.168755], [376.85471, -46.779718, -97.362305],
     [375.58349, -76.146617, -98.692436], [374.237958, -103.272104, -99.347633]],
    [[408.624399, 84.06002, -96.847847], [406.87587, 58.424019, -97.912224], [406.967038, 29.816069, -97.929611],
     [405.124373, 4.49067, -96.798958], [404.950658, -21.613508, -97.63327], [403.298686, -48.959608, -98.358253],
     [403.13195, -75.439059, -98.489403], [400.618561, -103.080446, -98.169861]]]


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
        self.dashboard.DisableRobot()
        self.rotation = 1.09
        self.reset = [287.87, -11.85, 117.06, self.rotation]
        self.origin, self.vector_i, self.vector_j = self.learn_map()
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

        for i in range(8):
            for j in range(8):
                self.board_position_encoding[j][i][0] = self.origin[0] + i * self.vector_i[0] + j * self.vector_j[0]
                self.board_position_encoding[j][i][1] = self.origin[1] + i * self.vector_i[1] + j * self.vector_j[1]
                self.board_position_encoding[j][i][2] = self.origin[2]
                self.board_position_encoding[j][i][3] = self.rotation

        print('positions are all set.')

        self.void_pos = self.learn_void_pos()
        print('void position is set.')
        self.promotion_poses = {
            'q': [None, None, None, self.rotation],
            'b': [None, None, None, self.rotation],
            'r': [None, None, None, self.rotation],
            'n': [None, None, None, self.rotation]
        }

        self.learn_promotions(self.promotion_poses)

        self.word_to_pos = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        self.time_to_wait = 200

        self.dashboard.EnableRobot()
        self.reset_pos()

    # TODO: to be implemented
    def move_piece(self, action: str, capture: bool, castling: bool, en_passant: bool):
        """
        This method takes a chess action (in uci format) and performs it using the robotic arm.
        Note that there are multiple types of actions and each needs different sequences of actions to be performed by
        the robot:
        Simple move,
        Simple move with capture,
        Promotion,
        Promotion with capture,
        Castling
        :param en_passant: a boolean indicating whether to perform en passant action or not.
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
            self.simple_move(action, capture, en_passant)

    def simple_move(self, action: str, capture: bool, en_passant: bool):
        end_pos, start_pos = self.extract_pos(action)
        self.reset_pos()
        if capture:
            self.act(self.board_position_encoding[end_pos[0]][end_pos[1]], self.void_pos)
        elif en_passant:
            self.act(self.board_position_encoding[start_pos[0]][end_pos[1]], self.void_pos)

        self.act(self.board_position_encoding[start_pos[0]][start_pos[1]],
                 self.board_position_encoding[end_pos[0]][end_pos[1]])
        self.reset_pos()

    def promotion(self, action: str, capture: bool):
        end_pos, start_pos = self.extract_pos(action)
        self.reset_pos()
        if capture:
            self.act(self.board_position_encoding[end_pos[0]][end_pos[1]], self.void_pos)
        new_void = [self.void_pos[0], self.void_pos[1], self.void_pos[2] + 5, self.void_pos[3]]
        self.act(self.board_position_encoding[start_pos[0]][start_pos[1]], new_void)
        self.act(self.promotion_poses[action[-1]], self.board_position_encoding[end_pos[0]][end_pos[1]])
        self.reset_pos()

    def extract_pos(self, action):
        start_action = action[0:2]
        end_action = action[2:4]
        start_pos = [int(start_action[1]) - 1 if self.color == 1 else -1 * int(start_action[1]),
                     self.word_to_pos[start_action[0]] if self.color == 1 else -1 * self.word_to_pos[
                         start_action[0]] - 1]
        end_pos = [int(end_action[1]) - 1 if self.color == 1 else -1 * int(end_action[1]),
                   self.word_to_pos[end_action[0]] if self.color == 1 else -1 * self.word_to_pos[end_action[0]] - 1]
        return end_pos, start_pos

    def castling(self, action: str):
        end_pos, start_pos = self.extract_pos(action)
        self.reset_pos()
        self.act(self.board_position_encoding[start_pos[0]][start_pos[1]],
                 self.board_position_encoding[end_pos[0]][end_pos[1]])
        second_start_action = second_end_action = ''
        if self.color * start_pos[1] > self.color * end_pos[1]:  # queen side castling.
            if self.color == 1:
                second_start_action = f'a1'
                second_end_action = f'd1'
            else:
                second_start_action = f'a8'
                second_end_action = f'd8'
        elif self.color * start_pos[1] < self.color * end_pos[1]:  # king side castling.
            if self.color == 1:
                second_start_action = f'h1'
                second_end_action = f'f1'
            else:
                second_start_action = f'h8'
                second_end_action = f'f8'

        second_action = second_start_action + second_end_action
        second_end_pos, second_start_pos = self.extract_pos(second_action)
        self.act(self.board_position_encoding[second_start_pos[0]][second_start_pos[1]],
                 self.board_position_encoding[second_end_pos[0]][second_end_pos[1]])
        self.reset_pos()

    def act(self, start_pos, end_pos):
        """
        Performs an actual robot action. moves a chess piece from a starting position to an ending position.
        :param start_pos: starting position
        :param end_pos: ending position
        :return: nothing
        """
        delta = 5
        start_pos_delta = [start_pos[0], start_pos[1], start_pos[2] + delta, start_pos[3]]
        end_pos_delta = [end_pos[0], end_pos[1], end_pos[2] + delta, end_pos[3]]

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

    def reset_pos(self):
        """
        The starting position of the robot.
        :return: nothing
        """
        self.move.MovL(*self.reset)
        # self.dashboard.wait(self.time_to_wait * 10)

    def memories(self):
        poses = [[[] for j in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                input("proceed? ")
                pos = self.get_position()
                poses[i][j] = [float(pos[0]), float(pos[1]), float(pos[2])]
                print(f'pos {i}, {j}: {pos}')

        print(f'Memorised positions:\n{poses}')

    def learn_map(self):
        input("show the origin point in the board, then press enter.")
        pos = self.get_position()
        z = float(pos[2])
        origin = [float(pos[0]), float(pos[1]), z]
        input("show the bottom right point.")
        pos = self.get_position()
        br = [float(pos[0]), float(pos[1]), z]
        input("show the top left point.")
        pos = self.get_position()
        tl = [float(pos[0]), float(pos[1]), z]

        x0, y0 = origin[0], origin[1]
        x1, y1 = br[0], br[1]
        x2, y2 = tl[0], tl[1]

        learning_rate = 1e-5

        loss_history = []
        for i in range(500):
            z_o = x0 ** 2 + -(x1 + x2) * x0 + x1 * x2 + y0 ** 2 - (y1 + y2) * y0 + y1 * y2
            loss_history.append(1 / 2 * (z_o ** 2))
            dl_dz = z_o
            dl_dx0 = dl_dz * (2 * x0 - (x1 + x2))  # dl_dx = dl_dz * dz_dx0
            dl_dx1 = dl_dz * (x2 - x0)
            dl_dx2 = dl_dz * (x1 - x0)
            dl_dy0 = dl_dz * (2 * y0 - (y1 + y2))
            dl_dy1 = dl_dz * (y2 - y0)
            dl_dy2 = dl_dz * (y1 - y0)

            dl_dx0 *= learning_rate
            dl_dx1 *= learning_rate
            dl_dx2 *= learning_rate
            dl_dy0 *= learning_rate
            dl_dy1 *= learning_rate
            dl_dy2 *= learning_rate

            x0 -= dl_dx0
            x1 -= dl_dx1
            x2 -= dl_dx2
            y0 -= dl_dy0
            y1 -= dl_dy1
            y2 -= dl_dy2

        plt.plot(loss_history)
        plt.title('Map positions learning curve')
        plt.xlabel('Epochs')
        plt.ylabel('<a1 | a2>')
        plt.show()
        self.check_terminate()

        vector_i = [(x1 - x0) / 7, (y1 - y0) / 7, z, self.rotation]
        vector_j = [(x2 - x0) / 7, (y2 - y0) / 7, z, self.rotation]
        origin = [x0, y0, z, self.rotation]

        # now it's time to show the learned positions
        self.dashboard.EnableRobot()  # this can be changed
        self.reset_pos()
        self.move.MovL(*origin)
        self.dashboard.DO(1, 1)
        self.dashboard.wait(1000)
        self.dashboard.DO(1, 0)
        self.check_terminate()
        br_2 = [7 * vector_i[0] + origin[0], 7 * vector_i[1] + origin[1], z, self.rotation]
        self.move.MovL(*br_2)
        self.check_terminate()
        tl_2 = [7 * vector_j[0] + origin[0], 7 * vector_j[1] + origin[1], z, self.rotation]
        self.move.MovL(*tl_2)
        self.check_terminate()
        tr_2 = [7 * vector_i[0] + 7 * vector_j[0] + origin[0], 7 * vector_i[1] + 7 * vector_j[1] + origin[1], z,
                self.rotation]
        self.move.MovL(*tr_2)
        self.check_terminate()
        #self.reset_pos()
        self.dashboard.DisableRobot()

        return origin, vector_i, vector_j

    def learn_promotions(self, promotions):
        input('show the queen promotion position and then press enter.')
        pos = self.get_position()
        promotions['q'] = [float(pos[0]), float(pos[1]), float(pos[2]), self.rotation]

        input('show the bishop promotion position and then press enter.')
        pos = self.get_position()
        promotions['b'] = [float(pos[0]), float(pos[1]), float(pos[2]), self.rotation]

        input('show the rook promotion position and then press enter.')
        pos = self.get_position()
        promotions['r'] = [float(pos[0]), float(pos[1]), float(pos[2]), self.rotation]

        input('show the knight promotion position and then press enter.')
        pos = self.get_position()
        promotions['n'] = [float(pos[0]), float(pos[1]), float(pos[2]), self.rotation]

        print('promotion positions are all set.')

    def learn_void_pos(self):
        input('show the void position for capturing and then press enter.')
        pos = self.get_position()
        pos = [float(pos[0]), float(pos[1]), float(pos[2]), self.rotation]
        return pos

    def get_position(self):
        pos = self.dashboard.GetPose()
        pos = re.findall("[-+]?\d*\.\d+,\s*[-+]?\d*\.\d+,\s*[-+]?\d*\.\d+,\s*[-+]?\d*\.\d+", pos)[0]
        pos = pos.split(',')
        return pos

    def check_terminate(self):
        command = input('proceed (Y/n)? ')

        if not (command == 'Y' or command == ''):
            self.close_connection()
            print('process terminates')
            exit(0)

    def close_connection(self):
        self.dashboard.DisableRobot()
        self.dashboard.close()
        self.move.close()
        self.feed.close()


if __name__ == '__main__':
    """try:
        ip = "192.168.1.6"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("Establishing connection ...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<Connection Successful>!<")
    except Exception as e:
        print(":(Connection Failed:(")
        raise e"""
    ar = Arm(1)
    cap = False
    cas = False
    """ar.reset_pos()
    ar.dashboard.DO(1, 1)
    ar.dashboard.DO(1, 0)
    ar.dashboard.DisableRobot()
    ar.close_connection()
    exit(0)"""
    while True:
        comm = input('act: ')
        if comm == 'q':
            break
        if comm == 'r':
            ar.reset_pos()
            continue
        cap = True if input('capture? ') == '1' else False
        cas = True if input('castling? ') == '1' else False
        enp = True if input('en passant: ') == '1' else False
        ar.move_piece(comm, cap, cas, enp)

    ar.close_connection()
    """dashboard.EnableRobot()
    #move.MovL(217.57, 96.15, -100.90, 20.15) # BL
    move.MovL(406.12, -102.11, -80, 20.15) # Tr
    dashboard.DisableRobot()"""
