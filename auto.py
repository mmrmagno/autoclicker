import tkinter as tk
from tkinter import tkk
import threading
import time
from pynput.mouse import Button, Controller
from pynput import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.mouse = Controller()
        self.clicking = False
        self.delay = 1.0
        self.create_widgets()
        self.setup_hotkeys()

    def create_widgets(self):
        self.root.title("AutoClicker")
        self.root.geometry("300x150")

        tkk.Label(self.root, text="Click interval (seconds):").pack(pady=10)
        self.interval_entry = tkk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, "1.0")

        self.start_button = tkk.Button(self.root, text="Start", command=self.start_clicking)
        self.start_button.pack(pady=10)

        self.stop_button = tkk.Button(self.root, text="Stop", command=self.stop_clicking)
        self.stop_button.pack(pady=5)

        self.status_label = tkk.Label(self.root, text="Status: stopped")
        iself.status_label.pack(pady=10)

    def start_clicking(self):
        try:
            self.delay = float(self.interval_entry.get())
            self.clicking = True
            self.status_label.config(text="Status: Clicking")
            threading.Thread(target=self.clicker).start()
        except ValueError:
            self.status_label.config(text="Status: Invalid Interval")

    def stop_clicking(self):
        self.clicking = False
        self.status_label.config(text="Status: Stopped")

    def clicker(self):
        while self.clicking:
            self.mouse.click(Button.left, 1)
            time.sleep(self.delay)

    def setup_hotkeys(self):
        def on_press(key):
            try:
                if key.char == 's':
                    self.start_clicking()
                elif key.char == 'x':
                    self.stop_clicking()
            except AttributeError:
                pass
        
        self.listener = keyboard.listener(on_press=on_press)
        self.listener.start()

    def on_closing(self):
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.TK()
    app = AutoClicker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()