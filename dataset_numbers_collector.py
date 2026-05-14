import serial
import threading
import time
import csv
import os

# =========================================
# CONFIG
# =========================================
PORT = "COM7"
BAUD = 115200

SAMPLES_PER_LABEL = 300

FILENAME = "Arabic_Numbers_Left_Hand.csv"

# =========================================
# SHARED VARIABLES
# =========================================
frame = None

lock = threading.Lock()

# =========================================
# CSV HEADER
# =========================================
header = [
    "flex1",
    "flex2",
    "flex3",
    "flex4",
    "flex5",

    "accX",
    "accY",
    "accZ",

    "gyroX",
    "gyroY",
    "gyroZ",

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
# SERIAL READER
# =========================================
def read_serial():

    global frame

    ser = serial.Serial(PORT, BAUD, timeout=1)

    time.sleep(2)

    print("✅ LEFT hand connected")

    while True:

        try:

            line = ser.readline().decode(errors="ignore").strip()

            if line.startswith("LEFT,"):

                data = line.replace("LEFT,", "").split(",")

                if len(data) >= 11:

                    with lock:
                        frame = data

        except:
            pass

# =========================================
# START THREAD
# =========================================
threading.Thread(target=read_serial, daemon=True).start()

print("\n🔥 Left Hand Numbers Dataset Collector Ready")

print("\nAvailable labels:")
print("0 1 2 3 4 5 6 7 8 9")

# =========================================
# MAIN LOOP
# =========================================
while True:

    label = input("\nEnter number label (or type stop): ")

    if label.lower() == "stop":

        print("🛑 Program stopped")

        break

    print(f"\n🎯 Recording number: {label}")

    dataset = []

    count = 0

    # =====================================
    # COLLECT 300 FRAMES
    # =====================================
    while count < SAMPLES_PER_LABEL:

        time.sleep(0.05)

        with lock:

            if frame is not None:

                row = frame + [label]

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

    print(f"\n✅ Saved number '{label}' to {FILENAME}")

    # =====================================
    # CONTINUE OR STOP
    # =====================================
    choice = input("\n[a] Add another number   [s] Stop : ")

    if choice.lower() == "s":

        print("\n🛑 Dataset collection finished")

        break