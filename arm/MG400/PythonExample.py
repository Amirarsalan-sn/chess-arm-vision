import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np

PARAMS = 0


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


if __name__ == '__main__':
    dashboard, move, feed = connect_robot()

    """
    ************************************
    ************************************
        if PARAMS  Does the conditional compilation instruction have parameters?
            0  The command does not contain any parameters
            1   Instructions with parameters
            
        Examples include the following instructions：
            EnableRobot
            DisableRobot
            DO
            AccJ
            SetArmOrientation
            RunScript
            PositiveSolution
            InverseSolution
            ModbusCreate
            GetHoldRegs
            DOGroup
            MovL
            MovLIO
            MoveJog
            Circle
    """

    """
    ************************************
    ************************************
     * Command: EnableRobot
     * Function: Enable the robot
    """
    if PARAMS:
        dashboard.EnableRobot()  # No parameters
    else:
        load = 0.1
        centerX = 0.1
        centerY = 0.1
        centerZ = 0.1
        dashboard.EnableRobot(load)  # One parameter

        dashboard.EnableRobot(load, centerX, centerY, centerZ)  # Four parameters

    """
    ************************************
    ************************************
     * Command: DisableRobotexit
     * Function: Disable the robot
    """
    dashboard.DisableRobot()  # 无参数

    """
    ************************************
    ************************************
     * Instruction: DO
     * Function: Set the digital output port status (queue instruction)
    """
    index = 1
    status = 1
    dashboard.DO(index, status)

    """
     *******************************
     *******************************
     * Command: AccJ
     * Function: Set the joint acceleration ratio. This command is only valid for MovJ, MovJIO, MovJR, and JointMovJ 
     commands.
    """
    index = 1
    dashboard.AccJ(index)

    """
     ******************************
     ******************************
     * Command: SetArmOrientation
     * Function: Set the arm orientation.
    """
    if PARAMS:
        LorR = 1
        dashboard.SetArmOrientation(LorR)  # 1 parameter
    else:
        LorR = 1
        UorD = 1
        ForN = 1
        Config = 1
        dashboard.SetArmOrientation(LorR, UorD, ForN, Config)  # 4 parameters

    """
    ************************************
    ************************************
     * Command: RunScript
     * Function: Run lua script.
    """
    name = "luaname"
    dashboard.RunScript(name)

    """
    ************************************
    ************************************
     * Command: PositiveSolution
     * Function: Positive solution. (Given the angles of each robot joint, calculate the spatial position of the robot 
     end)
    """
    J1 = 0.1
    J2 = 0.1
    J3 = 0.1
    J4 = 0.1
    User = 1
    Tool = 1
    dashboard.PositiveSolution(J1, J2, J3, J4, User, Tool)  # 1 parameter

    """
    ************************************
    ************************************
     * Command: InverseSolution
     * Function: Inverse solution. (Given the position and posture of the robot end, calculate the angle value of each 
     joint of the robot)
    """
    if PARAMS:
        J1 = 0.1
        J2 = 0.1
        J3 = 0.1
        J4 = 0.1
        User = 1
        Tool = 1
        dashboard.InverseSolution(J1, J2, J3, J4, User, Tool)  # 1个参数
    else:
        J1 = 0.1
        J2 = 0.1
        J3 = 0.1
        J4 = 0.1
        User = 1
        Tool = 1
        isJointNear = 1
        JointNear = "JointNear"
        dashboard.InverseSolution(J1, J2, J3, J4, User, Tool, isJointNear, JointNear)

    """
    ************************************
    ************************************
     * Command: ModbusCreate
     * Function: Create a modbus master station
    """
    if PARAMS:
        ip = "192.168.1.6"
        port = 29999
        slave_id = 1
        dashboard.ModbusCreate(ip, port, slave_id)  # 3 parameters
    else:
        ip = "192.168.1.6"
        port = 29999
        slave_id = 1
        isRTU = 1
        dashboard.ModbusCreate(ip, port, slave_id, isRTU)  # 4 parameters

    """
    ************************************
    ************************************
     * Instruction: GetHoldRegs
     * Function: Read holding registers.
       """
    if PARAMS:
        index = 1
        addr = 1
        count = 1
        dashboard.GetHoldRegs(index, addr, count)  # 3 parameters
    else:
        index = 1
        addr = 1
        count = 1
        valType = "valType"
        dashboard.GetHoldRegs(index, addr, count, valType)  # 4 parameters

    """
    ************************************
    ************************************
     * Command: DOGroup
     * Function: Set the output group port status (supports up to 64 parameters)
    """
    if PARAMS:
        index = 1
        value = 1
        dashboard.DOGroup(index, value)  # 2 Parameters
    else:
        index = 1
        value = 1
        index2 = 1
        value2 = 1
        index32 = 1
        value32 = 1
        dashboard.DOGroup(index, value, index2, value2, index32, value32)  # 64 parameters (parameters omitted)

    """
    ************************************
    ************************************
     * Command: MovL
     * Function: Point-to-point motion, the target point is a Cartesian point
    """
    if PARAMS:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        move.MovL(x, y, z, r)  # 无可选参数
    else:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        userparam = "User=1"
        toolparam = "Tool=1"
        speedlparam = "SpeedL=1"
        acclparam = "AccL=1"
        cpparam = "CP=1"
        move.MovL(x, y, z, r, userparam)  # Set user optional parameters order can be changed
        move.MovL(x, y, z, r, userparam, toolparam)  # Setting up the user tool
        move.MovL(x, y, z, r, userparam, toolparam, speedlparam, )  # Set user tool speedl
        move.MovL(x, y, z, r, userparam, toolparam, speedlparam, acclparam)  # Set user user tool speedl accl
        move.MovL(x, y, z, r, userparam, toolparam, speedlparam, acclparam, cpparam)  # Set user tool speedl accl cp

    """
    ************************************
    ************************************
    * Command: Arc
    * Function: Move from the current position to the target position in the Cartesian coordinate system by circular 
    interpolation.
    This command needs to be combined with other motion commands to determine the starting point of the arc.
    """
    if PARAMS:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        x2 = 1.0
        y2 = 1.0
        z2 = 1.0
        r2 = 1.0
        move.Arc(x, y, z, r, x2, y2, z2, r2)  # No optional parameters
    else:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        x2 = 1.0
        y2 = 1.0
        z2 = 1.0
        r2 = 1.0
        userparam = "User=1"
        toolparam = "Tool=1"
        speedlparam = "SpeedL=1"
        acclparam = "AccL=1"
        cpparam = "CP=1"
        move.Arc(x, y, z, r, x2, y2, z2, r2, cpparam, userparam, speedlparam, toolparam, speedlparam,
                 acclparam)  # The order of user tools is not fixed and can be changed

    """
    ************************************
    ************************************
     * Command: MovLIO
     * Function: Set the digital output port status in parallel during linear motion, and the target point is a 
     Cartesian point.
    """
    if PARAMS:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        Mode = 1
        Distance = 1
        Index = 1
        Status = 1
        move.MovLIO(x, y, z, r, Mode, Distance, Index, Status)  # 无可选参数
    else:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        Mode = 1
        Distance = 1
        Index = 1
        Status = 1
        userparam = "User=1"
        toolparam = "Tool=1"
        speedlparam = "SpeedL=1"
        acclparam = "AccL=1"
        cpparam = "CP=1"
        move.MovLIO(x, y, z, r, Mode, Distance, Index, Status, cpparam, userparam, speedlparam, toolparam, speedlparam,
                    acclparam)  # The order of user tools is not fixed and can be changed

    """
    ************************************
    ************************************
     * Command: MoveJog
     * Function: Jog motion, non-fixed distance motion
    """
    if PARAMS:
        axisID = ""
        move.MoveJog(axisID)
    else:
        axisID = "j1+"
        CoordType = "CoordType=0"
        userparam = "User=0"
        toolparam = "Tool=0"
        move.MoveJog(axisID, CoordType, userparam, toolparam)

        # Send the MoveJog() stop command to control the robot to stop moving
    move.MoveJog()

    """
    ************************************
    ************************************
     * Command: Circle
     * Function: Full circle movement, only valid for Cartesian points.
    """
    if PARAMS:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        count = 1
        move.Circle(x, y, z, r, count)
    else:
        x = 1.0
        y = 1.0
        z = 1.0
        r = 1.0
        count = 1
        userparam = "User=0"
        toolparam = "Tool=0"
        speedlparam = "SpeedL=R"
        acclparam = "AccL=R"
        move.Circle(x, y, z, r, count, userparam, toolparam, speedlparam, acclparam)
