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
LINES = 267  # GPIO lines for 4 servos (Adjust these according to your setup)

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
        value = request.get_values()[0]  # Mendapatkan nilai dari line pertama di LINES

        if value == Value.ACTIVE:  # Periksa jika nilainya ACTIVE
            print("Garis terdeteksi")
        else:  # Nilai INACTIVE
            print("Tidak ada garis")

        # Tunda sedikit sebelum membaca ulang
        time.sleep(0.1)