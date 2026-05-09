import socket
import threading
import tkinter as tk

LEFT_IP = "192.168.0.118"    # change this
RIGHT_IP = "192.168.0.198"   # change this
PORT = 80

data = {
    "LEFT": {
        "flex": [0, 0, 0, 0, 0],
        "acc": [0, 0, 0],
        "gyro": [0, 0, 0],
        "status": "Disconnected"
    },
    "RIGHT": {
        "flex": [0, 0, 0, 0, 0],
        "acc": [0, 0, 0],
        "gyro": [0, 0, 0],
        "status": "Disconnected"
    }
}

def read_hand(ip, hand_name):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, PORT))
            data[hand_name]["status"] = "Connected"

            buffer = ""

            while True:
                chunk = s.recv(1024).decode(errors="ignore")
                if not chunk:
                    break

                buffer += chunk

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    values = line.strip().split(",")

                    if len(values) == 12:
                        hand = values[0]

                        flex = list(map(int, values[1:6]))
                        acc = list(map(int, values[6:9]))
                        gyro = list(map(int, values[9:12]))

                        data[hand]["flex"] = flex
                        data[hand]["acc"] = acc
                        data[hand]["gyro"] = gyro
                        data[hand]["status"] = "Connected"

        except:
            data[hand_name]["status"] = "Disconnected"


def update_screen():
    left_text.set(
        f"LEFT HAND\n"
        f"Status: {data['LEFT']['status']}\n\n"
        f"Flex 1: {data['LEFT']['flex'][0]}\n"
        f"Flex 2: {data['LEFT']['flex'][1]}\n"
        f"Flex 3: {data['LEFT']['flex'][2]}\n"
        f"Flex 4: {data['LEFT']['flex'][3]}\n"
        f"Flex 5: {data['LEFT']['flex'][4]}\n\n"
        f"Acc X: {data['LEFT']['acc'][0]}\n"
        f"Acc Y: {data['LEFT']['acc'][1]}\n"
        f"Acc Z: {data['LEFT']['acc'][2]}\n\n"
        f"Gyro X: {data['LEFT']['gyro'][0]}\n"
        f"Gyro Y: {data['LEFT']['gyro'][1]}\n"
        f"Gyro Z: {data['LEFT']['gyro'][2]}"
    )

    right_text.set(
        f"RIGHT HAND\n"
        f"Status: {data['RIGHT']['status']}\n\n"
        f"Flex 1: {data['RIGHT']['flex'][0]}\n"
        f"Flex 2: {data['RIGHT']['flex'][1]}\n"
        f"Flex 3: {data['RIGHT']['flex'][2]}\n"
        f"Flex 4: {data['RIGHT']['flex'][3]}\n"
        f"Flex 5: {data['RIGHT']['flex'][4]}\n\n"
        f"Acc X: {data['RIGHT']['acc'][0]}\n"
        f"Acc Y: {data['RIGHT']['acc'][1]}\n"
        f"Acc Z: {data['RIGHT']['acc'][2]}\n\n"
        f"Gyro X: {data['RIGHT']['gyro'][0]}\n"
        f"Gyro Y: {data['RIGHT']['gyro'][1]}\n"
        f"Gyro Z: {data['RIGHT']['gyro'][2]}"
    )

    root.after(200, update_screen)


threading.Thread(target=read_hand, args=(LEFT_IP, "LEFT"), daemon=True).start()
threading.Thread(target=read_hand, args=(RIGHT_IP, "RIGHT"), daemon=True).start()

root = tk.Tk()
root.title("Two Hands Sensor Monitor")
root.geometry("700x500")

left_text = tk.StringVar()
right_text = tk.StringVar()

left_label = tk.Label(root, textvariable=left_text, font=("Arial", 14), justify="left")
left_label.pack(side="left", padx=40, pady=30)

right_label = tk.Label(root, textvariable=right_text, font=("Arial", 14), justify="left")
right_label.pack(side="right", padx=40, pady=30)

update_screen()
root.mainloop()