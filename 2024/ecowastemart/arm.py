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
from gpiod.line import Direction, Value

LINE = 32  # GPIO line for PWM
FREQUENCY = 50  # Servo PWM frequency (50Hz is typical for servos)
MIN_DUTY_CYCLE = 2.5  # Minimum duty cycle for 0 degree (usually 2.5%)
MAX_DUTY_CYCLE = 12.5  # Maximum duty cycle for 180 degree (usually 12.5%)

def set_servo_angle(request, line, angle):
    # Convert the angle to duty cycle
    duty_cycle = MIN_DUTY_CYCLE + (angle / 180.0) * (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE)
    pulse_width = duty_cycle / 100.0  # Convert to pulse width percentage
    request.set_value(line, Value.ACTIVE)
    time.sleep(pulse_width / FREQUENCY)
    request.set_value(line, Value.INACTIVE)
    time.sleep((1.0 / FREQUENCY) - (pulse_width / FREQUENCY))

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="servo-control",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.INACTIVE
        )
    },
) as request:
    while True:
        # Move servo from 0 to 180 degrees
        for angle in range(0, 181, 10):
            set_servo_angle(request, LINE, angle)
            print(f"Servo at {angle} degrees")
            time.sleep(0.5)

        # Move servo from 180 to 0 degrees
        for angle in range(180, -1, -10):
            set_servo_angle(request, LINE, angle)
            print(f"Servo at {angle} degrees")
            time.sleep(0.5)