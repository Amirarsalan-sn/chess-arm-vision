from Brain import StockFishOpponent
from vision.Eye import Eye
from arm.Arm import Arm
import bluetooth
import time


class Play:
    def __init__(self, color=1):
        self.color = color  # -1 for black
        self.eye = Eye(color)
        self.brain = StockFishOpponent("D:/stockfish/stockfish-windows-x86-64.exe")
        self.arm = Arm(color)
        self.find_bluetooth_devices()
        self.connect_to_device()

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

    @staticmethod
    def find_bluetooth_devices():
        nearby_devices = bluetooth.discover_devices(lookup_names=True)

        print("Found {} devices.".format(len(nearby_devices)))

        for addr, name in nearby_devices:
            print("  Address: {}, Name: {}".format(addr, name))

    def connect_to_device(self):
        # Create a Bluetooth socket
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # Bind the socket to any port
        port = bluetooth.PORT_ANY
        server_sock.bind(("", port))

        # Start listening on the socket
        server_sock.listen(1)

        # Get the port number
        port = server_sock.getsockname()[1]

        print(f"Listening on port {port}")

        # Advertise the service
        bluetooth.advertise_service(server_sock, "BluetoothServer",
                                    service_classes=[bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        # Accept a connection
        self.client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")

    def receive_order(self):
        try:
            while True:
                # Receive data from the client
                data = self.client_sock.recv(1024)
                if data:
                    break
                print(f"Received: {data}")

                # Parse the received data (example: convert to string)
                parsed_data = data.decode('utf-8')
                print(f"Parsed data: {parsed_data}")
        except OSError as e:
            print(f"AN ERROR OCCURRED RECEIVING THE ORDERS: {e}")

    def main_flow(self):
        if self.color == 1:
            self.receive_order()
            player_action = self.brain.step('white begins')
            self.arm.move(player_action, False)

        while True:
            self.receive_order()
            new_board = self.eye.look()
            opponent_action, capture = self.differentiate(new_board)
            player_action = self.brain.step(opponent_action)
            self.arm.move(player_action, capture)

    def differentiate(self, new_board) -> str:
        pass

    def end(self):
        self.arm.close_connection()
        self.client_sock.close()


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
