import threading
import time
import pyautogui
import tkinter as tk
from tkinter import ttk
import keyboard  # import keyboard modul

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")

        self.running = False
        self.delay = 0.1  # default interval between clicks

        self.start_button = ttk.Button(root, text="Start", command=self.start_clicking)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.speed_label = ttk.Label(root, text=f"Speed (seconds): {self.delay}")
        self.speed_label.pack(pady=5)

        self.speed_scale = ttk.Scale(root, from_=0.01, to=1, value=self.delay, command=self.change_speed)
        self.speed_scale.pack(pady=5)

        self.thread = None

        # Registracija globalnih hotkey-eva:
        keyboard.add_hotkey('*', self.toggle_running)  # * za start/stop
        keyboard.add_hotkey('+', self.speed_up)        # + za ubrzanje
        keyboard.add_hotkey('-', self.slow_down)       # - za usporavanje

    def change_speed(self, val):
        self.delay = float(val)
        self.speed_label.config(text=f"Speed (seconds): {self.delay:.2f}")

    def clicker(self):
        while self.running:
            pyautogui.click()
            time.sleep(self.delay)

    def start_clicking(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.clicker)
            self.thread.daemon = True
            self.thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_clicking(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def toggle_running(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def speed_up(self):
        new_speed = max(0.01, self.delay - 0.01)
        self.speed_scale.set(new_speed)  # ovo poziva change_speed automatski

    def slow_down(self):
        new_speed = min(1, self.delay + 0.01)
        self.speed_scale.set(new_speed)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
