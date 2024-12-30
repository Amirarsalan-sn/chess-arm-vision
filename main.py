from arm.MG400.dobot_api import DobotApiDashboard, DobotApiMove, DobotApi
import time


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


def reset_pos():
    print(move.MovL(234, -1, 0.58, 34.6))


def down():
    print(move.MovL(234, -1, -112, 34.6))


time_to_wait = 200

if __name__ == "__main__":
    dashboard, move, feed = connect_robot()
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
    feed.close()
