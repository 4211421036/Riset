try:
    import time
    import gpiod
    from gpiod.line import Direction, Value
except ImportError:
    import os
    os.system("sudo apt install python3-pip")
    os.system("pip install gpiod")

import time
import gpiod
from gpiod.line import Direction

# Constants for the motor driver and sensors
MOTOR_LEFT_FORWARD = 259   # GPIO pin for left motor forward
MOTOR_LEFT_BACKWARD = 260  # GPIO pin for left motor backward
MOTOR_RIGHT_FORWARD = 257  # GPIO pin for right motor forward
MOTOR_RIGHT_BACKWARD = 272 # GPIO pin for right motor backward

IR_SENSOR_LEFT = 258       # GPIO pin for left IR sensor
IR_SENSOR_RIGHT = 271      # GPIO pin for right IR sensor

# Setup GPIO lines for motors and sensors
MOTOR_PINS = [MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD]
SENSOR_PINS = [IR_SENSOR_LEFT, IR_SENSOR_RIGHT]

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="line-follower",
    config={
        line: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE) for line in MOTOR_PINS
    } | {
        line: gpiod.LineSettings(direction=Direction.INPUT) for line in SENSOR_PINS
    }
) as request:

    def motor_forward():
        request.set_value(MOTOR_LEFT_FORWARD, Value.ACTIVE)
        request.set_value(MOTOR_LEFT_BACKWARD, Value.INACTIVE)
        request.set_value(MOTOR_RIGHT_FORWARD, Value.ACTIVE)
        request.set_value(MOTOR_RIGHT_BACKWARD, Value.INACTIVE)

    def motor_backward():
        request.set_value(MOTOR_LEFT_FORWARD, Value.INACTIVE)
        request.set_value(MOTOR_LEFT_BACKWARD, Value.ACTIVE)
        request.set_value(MOTOR_RIGHT_FORWARD, Value.INACTIVE)
        request.set_value(MOTOR_RIGHT_BACKWARD, Value.ACTIVE)

    def motor_left():
        request.set_value(MOTOR_LEFT_FORWARD, Value.INACTIVE)
        request.set_value(MOTOR_LEFT_BACKWARD, Value.ACTIVE)
        request.set_value(MOTOR_RIGHT_FORWARD, Value.ACTIVE)
        request.set_value(MOTOR_RIGHT_BACKWARD, Value.INACTIVE)

    def motor_right():
        request.set_value(MOTOR_LEFT_FORWARD, Value.ACTIVE)
        request.set_value(MOTOR_LEFT_BACKWARD, Value.INACTIVE)
        request.set_value(MOTOR_RIGHT_FORWARD, Value.INACTIVE)
        request.set_value(MOTOR_RIGHT_BACKWARD, Value.ACTIVE)

    def motor_stop():
        for pin in MOTOR_PINS:
            request.set_value(pin, Value.INACTIVE)

    while True:
        left_sensor = request.get_value(IR_SENSOR_LEFT)
        right_sensor = request.get_value(IR_SENSOR_RIGHT)

        if left_sensor == Value.INACTIVE and right_sensor == Value.INACTIVE:
            motor_forward()  # Both sensors detect the line, move forward
        elif left_sensor == Value.ACTIVE and right_sensor == Value.INACTIVE:
            motor_right()  # Left sensor detects the line, turn right
        elif left_sensor == Value.INACTIVE and right_sensor == Value.ACTIVE:
            motor_left()  # Right sensor detects the line, turn left
        else:
            motor_stop()  # Both sensors don't detect the line, stop

        time.sleep(0.1)
