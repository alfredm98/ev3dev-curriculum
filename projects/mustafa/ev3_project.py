#!/usr/bin/env python3
# Alfred Mustafa
# CSSE120
# Final Project

import ev3dev.ev3 as ev3
import robot_controller as robo
import time


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print(" Drive polygon")
    print("--------------------------------------------")
    ev3.Sound.speak("Drive polygon").wait()

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()
    dc = DataContainer()

    # DONE: 4. Add the necessary IR handler callbacks as per the instructions above.
    # Remote control channel 1 is for driving the crawler tracks around (none of these functions exist yet below).
    # Remote control channel 2 is for moving the arm up and down (all of these functions already exist below).

    rc1 = ev3.RemoteControl(channel=1)
    rc1.on_red_up = lambda state: left_move(state, robot)
    rc1.on_blue_up = lambda state: right_move(state, robot)

    rc2 = ev3.RemoteControl(channel=2)
    rc2.on_red_up = lambda state: handle_arm_up_button(state, robot)
    rc2.on_red_down = lambda state: handle_arm_down_button(state, robot)

    # For our standard shutdown button.
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    robot.arm_calibration()  # Start with an arm calibration in this program.

    while dc.running:
        # DONE: 5. Process the RemoteControl objects.
        btn.process()
        rc1.process()
        rc2.process()
        time.sleep(0.01)

    # DONE: 2. Have everyone talk about this problem together then pick one  member to modify libs/robot_controller.py
    # as necessary to implement the method below as per the instructions in the opening doc string. Once the code has
    # been tested and shown to work, then have that person commit their work.  All other team members need to do a
    # VCS --> Update project...
    # Once the library is implemented any team member should be able to run his code as stated in todo3.
    robot.shutdown()


def left_move(state, robot):
    if state:
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=900)
    else:
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action="brake")


def right_move(state, robot):
    if state:
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=900)
    else:
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action="brake")


def handle_arm_up_button(button_state, robot):
    if button_state:
        robot.arm_up()


def handle_arm_down_button(button_state, robot):
    if button_state:
        robot.arm_down()


def handle_calibrate_button(button_state, robot):
    if button_state:
        robot.arm_calibration()


def handle_shutdown(button_state, dc):
    if button_state:
        dc.running = False


main()
