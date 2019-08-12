"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""


    def drive_inches(self, inches_target, speed_deg_per_second):

        ev3.Sound.speak("Get out of the way").wait()

        # Connect two large motors on output ports B and C
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected

        speed_sp = speed_deg_per_second
        distance = inches_target
        left_motor.run_to_rel_pos(position_sp=distance * 90, speed_sp=speed_sp)
        right_motor.run_to_rel_pos(position_sp=distance * 90, speed_sp=speed_sp)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        left_motor.stop(stop_action="brake")
        right_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def turn(self, turn_degrees, speed_deg_per_second):

        print("Turning...")
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        motor_turns_deg = 480*(turn_degrees/90)  # May require some tuning depending on your surface!
        left_motor.run_to_rel_pos(position_sp=motor_turns_deg, speed_sp=speed_deg_per_second)
        right_motor.run_to_rel_pos(position_sp=-motor_turns_deg, speed_sp=speed_deg_per_second)

        left_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Wait for the turn to finish
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Wait for the turn to finish
        ev3.Sound.beep().wait()  # Fun little beep
