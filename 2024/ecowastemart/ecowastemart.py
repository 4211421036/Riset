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

# Constants for the PWM
LINES = [267, 270, 269, 268]  # GPIO lines for 4 servos (Adjust these according to your setup)
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
        line: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.INACTIVE
        )
        for line in LINES
    },
) as request:
    while True:
        # Define different movements for each servo
        for angle in range(0, 181, 10):
            set_servo_angle(request, LINES[0], angle)  # Servo 1 moves 0 to 180
            set_servo_angle(request, LINES[1], 180 - angle)  # Servo 2 moves 180 to 0
            set_servo_angle(request, LINES[2], angle // 2)  # Servo 3 moves 0 to 90
            set_servo_angle(request, LINES[3], (angle + 90) % 180)  # Servo 4 moves in a different pattern
            print(f"Servo 1 at {angle} degrees, Servo 2 at {180 - angle} degrees, Servo 3 at {angle // 2} degrees, Servo 4 at {(angle + 90) % 180} degrees")
            time.sleep(0.5)

        # Move servos back in reverse order
        for angle in range(180, -1, -10):
            set_servo_angle(request, LINES[0], angle)
            set_servo_angle(request, LINES[1], 180 - angle)
            set_servo_angle(request, LINES[2], angle // 2)
            set_servo_angle(request, LINES[3], (angle + 90) % 180)
            print(f"Servo 1 at {angle} degrees, Servo 2 at {180 - angle} degrees, Servo 3 at {angle // 2} degrees, Servo 4 at {(angle + 90) % 180} degrees")
            time.sleep(0.5)

