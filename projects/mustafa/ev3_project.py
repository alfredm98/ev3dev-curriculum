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
    print("Final Project")
    print("--------------------------------------------")
    ev3.Sound.speak("Final Project").wait()

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()
    dc = DataContainer()

    # Remote control channel 1 is for driving the crawler tracks around (none of these functions exist yet below).
    # Remote control channel 2 is for moving the arm up and down (all of these functions already exist below).

    rc1 = ev3.RemoteControl(channel=1)
    rc1.on_red_up = lambda state: left_move(state, robot)
    rc1.on_blue_up = lambda state: right_move(state, robot)

    rc2 = ev3.RemoteControl(channel=2)
    rc2.on_red_up = lambda state: handle_arm_up_button(state, robot)
    rc2.on_red_down = lambda state: handle_arm_down_button(state, robot)

    rc3 = ev3.RemoteControl(channel=3)
    rc3.on_red_up = lambda state: stack(state, robot)
    rc3.on_red_down = lambda state: dance(state, robot)
    rc3.on_blue_up = lambda state: play_song(state)

    rc4 = ev3.RemoteControl(channel=4)
    rc4.on_red_up = lambda state: go_crazy(state, dc)
    rc4.on_blue_down = lambda state: handle_shutdown(state, dc)

    # For our standard shutdown button.
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    robot.arm_calibration()  # Start with an arm calibration in this program.

    while dc.running:
        # DONE: 5. Process the RemoteControl objects.
        btn.process()
        rc1.process()
        rc2.process()
        rc3.process()
        rc4.process()
        time.sleep(0.01)

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


def stack(button_state, robot):
    if button_state:
        speed_sp = int(input("Enter a speed (0 to 900 dps): "))
        robot.stack(speed_sp)
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=-900)
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=-900)
        time.sleep(1)
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action='brake')
        robot.arm_down()


def dance(button_state, robot):
    if button_state:
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=900)
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=-900)
        time.sleep(0.4)
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=-900)
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=900)
        time.sleep(0.4)
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=900)
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=-900)
        time.sleep(0.4)
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=-900)
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=900)
        time.sleep(0.4)
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action='brake')


def go_crazy(button_state, robot):
    if button_state:
        ev3.LargeMotor(ev3.OUTPUT_B).run_forever(speed_sp=900)
        ev3.LargeMotor(ev3.OUTPUT_C).run_forever(speed_sp=-900)
        time.sleep(8)
        ev3.LargeMotor(ev3.OUTPUT_B).stop(stop_action='brake')
        ev3.LargeMotor(ev3.OUTPUT_C).stop(stop_action='brake')


def play_song(button_state):
    if button_state:
        print("Right button is pressed")
        play_wav_file()


def play_wav_file():
    # File from http://www.moviesoundclips.net/ev3.Sound.php?id=288
    # Had to convert it to a PCM signed 16-bit little-endian .wav file
    # http://audio.online-convert.com/convert-to-wav
    ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav")


main()
