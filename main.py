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
    dashboard.EnableRobot()  # No parameters
    input('proceed ? :')
    print(move.MovL(234, -1, 0.58, -81))
    print(move.MovL(305, 121, 0.58, -81))
    print(move.MovL(294, -153, 0.58, -81))
    print(move.MovL(407, -11, 0.58, -81))
    print(move.MovL(234, -1, 0.58, -81))

    input('proceed? :')
    dashboard.DisableRobot()  # 无参数
    dashboard.socket_dobot.close()
    move.socket_dobot.close()
    feed.socket_dobot.close()
