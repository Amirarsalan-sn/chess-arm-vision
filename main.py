from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from Brain import StockFishOpponent
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from vision.Eye import Eye
from arm.Arm import Arm
import pyttsx3
import time
import math

DEFAULT_VOLUME = 0.85


class Play:
    def __init__(self, color=1):
        self.color = color  # -1 for black
        assert self.color == 1 or self.color == -1, "player color can either be 1 or -1"

        self.eye = Eye(color)
        self.brain = StockFishOpponent("D:/stockfish/stockfish-windows-x86-64.exe")
        self.arm = Arm(color)
        self.set_volume()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('rate', 150)  # Speed of speech
        self.speaker.setProperty('volume', 1)

        self.map = [['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'],
                    ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
                    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
                    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
                    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
                    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
                    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
                    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']]

        self.board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                      ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]

        self.word_to_pos = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def set_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMasterVolumeLevelScalar(DEFAULT_VOLUME, None)
        print(f"Volume set to: {DEFAULT_VOLUME * 100:.0f}%")

    def get_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume.GetMasterVolumeLevelScalar()

    def receive_order(self):
        while True:
            time.sleep(3)  # Sleep for 3 second before checking the volume again
            current_volume = self.get_volume()

            if current_volume != DEFAULT_VOLUME:
                print(f"Volume changed to: {current_volume * 100:.0f}%")
                self.set_volume()
                break

    def main_flow(self):
        if self.color == 1:
            self.receive_order()
            player_action = self.brain.step('white begins')
            self.arm.move_piece(player_action, False, False, False)

        while True:
            self.receive_order()
            try:
                new_board = self.eye.look()
            except Exception as e:
                print(f'Exception at eye: {e}\n')
                flag = self.terminate_check()
                if flag:
                    break
                continue
            try:
                opponent_action = self.differentiate(new_board)
            except Exception as e:
                print(f'An exception occurred, either the opponent has made a mistake or it is due to in accuracy of '
                      f'system. Please rearrange the pieces and start again:\n{e}')
                flag = self.terminate_check()
                if flag:
                    break
                continue
            player_action, finish_stat = self.brain.step(opponent_action)
            if player_action is None:  # the game finished.
                game_result = f"Game finished with outcome: " + \
                              f"{'White won' if finish_stat == 1 else 'Black won' if finish_stat == -1 else 'Draw'}"
                print(game_result)
                self.speaker.say(game_result)
                self.speaker.runAndWait()
                break
            capture = self.is_capture(player_action)
            castling, en_passant = self.apply_player_action(player_action)
            self.arm.move_piece(player_action, capture, castling, en_passant)
            if finish_stat != 2:  # the game finished.
                game_result = f"Game finished with outcome: " + \
                              f"{'White won' if finish_stat == 1 else 'Black won' if finish_stat == -1 else 'Draw'}"
                print(game_result)
                self.speaker.say(game_result)
                self.speaker.runAndWait()
                break

        self.end()

    def differentiate(self, new_board) -> str:
        result = None
        moved_piece_before = {}
        moved_piece_after = {}

        for i in range(8):
            for j in range(8):
                if new_board[i][j] == self.board[i][j]:
                    continue

                if ((self.color == 1 and self.board[i][j].islower()) or (
                        self.color == -1 and self.board[i][j].isupper())) and (new_board[i][j] == ''):
                    moved_piece_before[self.board[i][j].lower()] = [i, j]
                elif ((self.color == 1 and new_board[i][j].islower()) or (
                        self.color == -1 and new_board[i][j].isupper())):
                    moved_piece_after[new_board[i][j].lower()] = [i, j]

        if len(moved_piece_before) == len(moved_piece_after) == 2:  # castling might have happened.
            if ('k' in moved_piece_before) and ('n' in moved_piece_before) and ('k' in moved_piece_after) and \
                    ('n' in moved_piece_after):
                if (self.color == 1 and moved_piece_before['k'][0] == moved_piece_after['k'][0] == 7) or (
                        self.color == -1 and moved_piece_before['k'][0] == moved_piece_after['k'][0] == 0):
                    result = self.map[moved_piece_before['k'][0]][moved_piece_before['k'][1]] \
                             + self.map[moved_piece_after['k'][0]][moved_piece_after['k'][1]]
        elif len(moved_piece_before) == len(moved_piece_after) == 1:  # it is a simple move or a promotion.
            if moved_piece_before.keys() == moved_piece_after.keys():  # it is a simple move.
                for key in moved_piece_before.keys():
                    result = self.map[moved_piece_before[key][0]][moved_piece_before[key][1]] \
                             + self.map[moved_piece_after[key][0]][moved_piece_after[key][1]]
            elif ('p' in moved_piece_before.keys()) and ('k' not in moved_piece_after.keys()):  # it is a promotion
                for key in moved_piece_after.keys():
                    if (self.color == 1 and moved_piece_after[key][0] == 0) or (
                            self.color == -1 and moved_piece_after[key][0] == 7):
                        result = self.map[moved_piece_before['p'][0]][moved_piece_before['p'][1]] \
                                 + self.map[moved_piece_after[key][0]][moved_piece_after[key][1]] + key

        elif result is None:  # None of the cases above were satisfied, the action or the received perception is illegal
            legal_actions = []
            for start_val in moved_piece_before.values():
                for end_val in moved_piece_after.values():
                    action = self.map[start_val[0]][start_val[1]] + self.map[end_val[0]][end_val[1]]
                    if self.brain.is_legal(action):
                        legal_actions.append(action)

            if len(legal_actions) == 1:
                result = legal_actions[0]
            else:
                raise Exception(f'None of the cases above were satisfied, the action or the received perception is '
                                f'illegal:\nbefore: {self.board}\nafter: {new_board}')

        if not self.brain.is_legal(result):
            raise Exception(f"An illegal action extracted, it is either due to the opponent's action or inaccuracy of "
                            f"the system's vision:\nbefore: {self.board}\nafter: {new_board}")

        self.apply_player_action(result, opponent=True)

        print(f'predicted action: {result}')
        return result

    # TODO:remember to implement en_passant detection.
    def apply_player_action(self, player_action: str, opponent=False):
        action_start = player_action[0:2]
        action_end = player_action[2:4]
        promotion = None
        castling = False

        if len(player_action) > 4:
            promotion = player_action[-1]

        start_pose = [int(action_start[1]) - 1, self.word_to_pos[action_start[0]]]
        end_pose = [int(action_end[1]) - 1, self.word_to_pos[action_end[0]]]

        piece_to_move = self.board[start_pose[0]][start_pose[1]]

        if piece_to_move.lower() == 'k' and (math.fabs(start_pose[1] - end_pose[1]) == 2):  # castling occurred.
            second_start_pose = None
            second_end_pose = None

            if start_pose[1] < end_pose[1]:  # king side castling.
                second_start_pose = [start_pose[0], 7]
                second_end_pose = [start_pose[0], 5]
            elif start_pose[1] > end_pose[1]:  # queen side castling.
                second_start_pose = [start_pose[0], 0]
                second_end_pose = [start_pose[0], 3]

            self.move(second_start_pose, second_end_pose)
            castling = True

        en_passant = self.brain.is_en_passant(player_action)

        self.move(start_pose, end_pose)

        if promotion is not None:
            if opponent:
                if self.color == 1:
                    self.map[end_pose[0]][end_pose[1]] = promotion.lower()
                elif self.color == -1:
                    self.map[end_pose[0]][end_pose[1]] = promotion.upper()
            else:
                if self.color == 1:
                    self.map[end_pose[0]][end_pose[1]] = promotion.upper()
                elif self.color == -1:
                    self.map[end_pose[0]][end_pose[1]] = promotion.lower()

        if en_passant:
            self.map[start_pose[0]][end_pose[1]] = ''

        return castling, en_passant

    def is_capture(self, player_action) -> bool:
        action_end = player_action[2:4]

        end_piece = self.map[action_end[0]][action_end[1]]

        if end_piece == '':
            return False

        elif (self.color == 1 and end_piece.isupper()) and (self.color == -1 and end_piece.islower()):
            raise Exception('Player is Capturing itself !!!')

        return True

    def move(self, start_pose, end_pose):
        piece_to_move = self.map[start_pose[0]][start_pose[1]]
        self.map[start_pose[0]][start_pose[1]] = ''
        self.map[end_pose[0]][end_pose[1]] = piece_to_move

    def terminate_check(self):
        while True:
            comm = input('wanna terminate the program (Y/n) ? ')
            if comm == 'Y' or comm == '':
                print('termination confirmed.')
                return True
            elif comm == 'n':
                print('program continues')
                return False
            print('invalid answer.')

    def end(self):
        self.arm.close_connection()


if __name__ == "__main__":
    """dashboard, move, feed = connect_robot()
    dashboard.EnableRobot()  # No parameters
    reset_pos()
    input('proceed ? :')
    dashboard.SetPayload(0.5)
    print(move.MovL(280.5, 105.8, -99.1, 34.6))
    #input('proceed ? :')
    dashboard.wait(time_to_wait)
    dashboard.DO(1, 1)
    # input('proceed ? :')
    dashboard.wait(time_to_wait)
    # input('proceed ? :')
    print(move.MovL(244.5, 0.48, 6.1, 34.6))
    print(move.MovL(286.3, -89.1, -102.3, 34.6))
    # input('proceed ? :')
    dashboard.wait(time_to_wait)
    dashboard.DO(1, 0)
    dashboard.wait(time_to_wait)
    reset_pos()
    dashboard.wait(2000)
    print(move.MovL(286.3, -89.1, -102.3, 34.6))
    # input('proceed ? :')
    dashboard.wait(time_to_wait)
    dashboard.DO(1, 1)
    dashboard.wait(time_to_wait)
    # input('proceed ? :')
    print(move.MovL(244.5, 0.48, 6.1, 34.6))
    print(move.MovL(280.5, 105.8, -99.1, 34.6))
    # input('proceed ? :')
    dashboard.wait(time_to_wait)
    dashboard.DO(1, 0)
    dashboard.wait(time_to_wait)
    reset_pos()
    # down()
    input('proceed? :')
    # dashboard.DOExecute(1, 1)

    dashboard.SetPayload(0)

    input('proceed? :')
    # dashboard.DOExecute(1, 0)
    dashboard.DisableRobot()  # 无参数

    dashboard.close()
    move.close()
    feed.close()"""

    player = Play()
    player.main_flow()
