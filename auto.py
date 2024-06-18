import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput.mouse import Button, Controller
from pynput import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.mouse = Controller()
        self.clicking = False
        self.holding = False
        self.delay = 1.0
        self.create_widgets()
        self.setup_hotkeys()

    def create_widgets(self):
        self.root.title("AutoClicker")
        self.root.geometry("300x200")

        ttk.Label(self.root, text="Click Interval (seconds):").pack(pady=10)
        self.interval_entry = ttk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, "1.0")

        self.click_type = tk.StringVar(value="click")
        ttk.Radiobutton(self.root, text="Auto Click", variable=self.click_type, value="click").pack(pady=5)
        ttk.Radiobutton(self.root, text="Hold Button", variable=self.click_type, value="hold").pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_action)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_action)
        self.stop_button.pack(pady=5)
        
        self.status_label = ttk.Label(self.root, text="Status: Stopped")
        self.status_label.pack(pady=10)

    def start_action(self):
        try:
            self.delay = float(self.interval_entry.get())
            if self.click_type.get() == "click":
                self.clicking = True
                self.holding = False
                threading.Thread(target=self.clicker).start()
            else:
                self.clicking = False
                self.holding = True
                threading.Thread(target=self.holder).start()
            self.status_label.config(text="Status: Running")
        except ValueError:
            self.status_label.config(text="Status: Invalid Interval")

    def stop_action(self):
        self.clicking = False
        self.holding = False
        self.status_label.config(text="Status: Stopped")

    def clicker(self):
        while self.clicking:
            self.mouse.click(Button.left, 1)
            time.sleep(self.delay)

    def holder(self):
        self.mouse.press(Button.left)
        while self.holding:
            time.sleep(0.1)
        self.mouse.release(Button.left)

    def setup_hotkeys(self):
        def on_press(key):
            try:
                if key.char == 's':
                    self.start_action()
                elif key.char == 'x':
                    self.stop_action()
            except AttributeError:
                pass

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def on_closing(self):
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()