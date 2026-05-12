import serial
import threading
import time
import csv
import os

# =========================================
# CONFIG
# =========================================
LEFT_PORT = "COM7"
RIGHT_PORT = "COM8"
BAUD = 115200

SAMPLES_PER_LABEL = 300

FILENAME = "Arabic_Sign_Language.csv"

# =========================================
# SHARED VARIABLES
# =========================================
left_frame = None
right_frame = None

lock = threading.Lock()

# =========================================
# CSV HEADER
# =========================================
header = [
    "left_flex_1",
    "left_flex_2",
    "left_flex_3",
    "left_flex_4",
    "left_flex_5",

    "left_acc_x",
    "left_acc_y",
    "left_acc_z",

    "left_gyro_x",
    "left_gyro_y",
    "left_gyro_z",

    "right_flex_1",
    "right_flex_2",
    "right_flex_3",
    "right_flex_4",
    "right_flex_5",

    "right_acc_x",
    "right_acc_y",
    "right_acc_z",

    "right_gyro_x",
    "right_gyro_y",
    "right_gyro_z",

    "label"
]

# =========================================
# CREATE CSV FILE IF NOT EXISTS
# =========================================
if not os.path.exists(FILENAME):

    with open(FILENAME, "w", newline="", encoding="utf-8-sig") as f:

        writer = csv.writer(f)

        writer.writerow(header)

# =========================================
# SERIAL READ THREADS
# =========================================
def read_left():

    global left_frame

    ser = serial.Serial(LEFT_PORT, BAUD, timeout=1)

    time.sleep(2)

    print("✅ LEFT hand connected")

    while True:

        try:

            line = ser.readline().decode(errors="ignore").strip()

            if line.startswith("LEFT,"):

                data = line.replace("LEFT,", "").split(",")

                if len(data) >= 11:

                    with lock:
                        left_frame = data

        except:
            pass


def read_right():

    global right_frame

    ser = serial.Serial(RIGHT_PORT, BAUD, timeout=1)

    time.sleep(2)

    print("✅ RIGHT hand connected")

    while True:

        try:

            line = ser.readline().decode(errors="ignore").strip()

            if line.startswith("RIGHT,"):

                data = line.replace("RIGHT,", "").split(",")

                if len(data) >= 11:

                    with lock:
                        right_frame = data

        except:
            pass

# =========================================
# START THREADS
# =========================================
threading.Thread(target=read_left, daemon=True).start()

threading.Thread(target=read_right, daemon=True).start()

print("\n🔥 Dual Hand Dataset Collector Ready")

# =========================================
# MAIN LOOP
# =========================================
while True:

    label = input("\nEnter label (or type stop): ")

    if label.lower() == "stop":

        print("🛑 Program stopped")

        break

    print(f"\n🎯 Recording label: {label}")

    dataset = []

    count = 0

    # =====================================
    # COLLECT 300 FRAMES
    # =====================================
    while count < SAMPLES_PER_LABEL:

        time.sleep(0.05)

        with lock:

            if left_frame is not None and right_frame is not None:

                row = left_frame + right_frame + [label]

                dataset.append(row)

                count += 1

                if count % 10 == 0:

                    print(f"{count}/{SAMPLES_PER_LABEL}")

    # =====================================
    # SAVE TO CSV
    # =====================================
    with open(FILENAME, "a", newline="", encoding="utf-8-sig") as f:

        writer = csv.writer(f)

        writer.writerows(dataset)

    print(f"\n✅ Saved '{label}' to {FILENAME}")

    # =====================================
    # CONTINUE OR STOP
    # =====================================
    choice = input("\n[a] Add another label   [s] Stop : ")

    if choice.lower() == "s":

        print("\n🛑 Dataset collection finished")

        break