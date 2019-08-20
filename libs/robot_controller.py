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
touch_sensor = ev3.TouchSensor()
assert touch_sensor
MAX_SPEED = 900
arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
assert arm_motor.connected

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

    def arm_calibration(self):
        """
        Runs the arm up until the touch sensor is hit then back to the bottom again, beeping at both locations.
        Once back at in the bottom position, gripper open, set the absolute encoder position to 0.  You are calibrated!
        The Snatch3r arm needs to move 14.2 revolutions to travel from the touch sensor to the open position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
          :type touch_sensor: ev3.TouchSensor
        """
        # DONE: 3. Implement the arm calibration movement by fixing the code below (it has many bugs).  It should to this:
        #   Command the arm_motor to run forever in the positive direction at max speed.
        #   Create an infinite while loop that will block code execution until the touch sensor's is_pressed value is True.
        #     Within that loop sleep for 0.01 to avoid running code too fast.
        #   Once past the loop the touch sensor must be pressed. So stop the arm motor quickly using the brake stop action.
        #   Make a beep sound
        #   Now move the arm_motor 14.2 revolutions in the negative direction relative to the current location
        #     Note the stop action and speed are already set correctly so we don't need to specify them again
        #   Block code execution by waiting for the arm to finish running
        #   Make a beep sound
        #   Set the arm encoder position to 0 (the last line below is correct to do that, it's new so no bug there)

        # Code that attempts to do this task but has MANY bugs (nearly 1 on every line).  Fix them!
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 5112
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=900)
        arm_motor.wait_while(ev3.Motor.STATE_STALLED)
        arm_motor.wait_while(ev3.Motor.STATE_HOLDING)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        """
        Moves the Snatch3r arm to the up position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
          :type touch_sensor: ev3.TouchSensor
        """
        # DONE: 4. Implement the arm up movement by fixing the code below
        # Command the arm_motor to run forever in the positive direction at max speed.
        # Create a while loop that will block code execution until the touch sensor is pressed.
        #   Within the loop sleep for 0.01 to avoid running code too fast.
        # Once past the loop the touch sensor must be pressed. Stop the arm motor using the brake stop action.
        # Make a beep sound

        # Code that attempts to do this task but has many bugs.  Fix them!
        arm_motor.run_to_rel_pos(position_sp=5112, speed_sp=MAX_SPEED)
        while touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        arm_motor.stop(stop_action="brake")

    def arm_down(self):
        """
        Moves the Snatch3r arm to the down position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
        """
        # DONE: 5. Implement the arm up movement by fixing the code below
        # Move the arm to the absolute position_sp of 0 at max speed.
        # Wait until the move completes
        # Make a beep sound

        # Code that attempts to do this task but has bugs.  Fix them.
        arm_motor.run_to_abs_pos(position_sp=0)
        arm_motor.wait_while(ev3.Motor.STATE_HOLDING)  # Blocks until the motor finishes running

    def shutdown(self):
        arm_motor.run_to_abs_pos(position_sp=0)
        arm_motor.wait_while(ev3.Motor.STATE_HOLDING)
        print("Goodbye")
        ev3.Sound.speak("Good bye").wait()

    def stack(self, speed_sp):
        self.arm_up()
        self.turn(180, speed_sp)

        arm_motor.run_to_abs_pos(position_sp=4000)
        arm_motor.wait_while(ev3.Motor.STATE_HOLDING)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

