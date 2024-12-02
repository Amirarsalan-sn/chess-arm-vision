from arm.MG400.dobot_api import DobotApiDashboard, DobotApiMove, DobotApi


def connect_robot():
    try:
        ip = "192.168.1.6"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("Establishing connection ...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<Connection Successful>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(Connection Failed:(")
        raise e


if __name__ == "__main__":
    dashboard, move, feed = connect_robot()

    print(move.MovL(100, 100, 100, 90))
    print(move.MovL(-100, 100, 100, 90))
    print(move.MovL(-100, -100, 100, 90))
    print(move.MovL(100, -100, 100, 90))
    print(move.MovL(100, 100, 100, 90))
