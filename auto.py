import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pynput.mouse import Button, Controller
from pynput import keyboard
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AutoClicker:
    def __init__(self, root, icon_path):
        self.root = root
        self.mouse = Controller()
        self.clicking = False
        self.holding = False
        self.delay = 1.0
        self.start_key = 's'
        self.stop_key = 'x'
        self.button = Button.left
        self.icon_path = icon_path
        self.tray_icon = None
        self.create_widgets()
        self.setup_hotkeys()
        self.setup_tray_icon()

    def create_widgets(self):
        self.root.title("AutoClicker")
        self.root.geometry("400x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e3f4f")

        self.root.iconphoto(False, ImageTk.PhotoImage(Image.open(self.icon_path).resize((64, 64))))

        # Menu
        menubar = tk.Menu(self.root, bg="#2e3f4f", fg="white")
        settings_menu = tk.Menu(menubar, tearoff=0, bg="#2e3f4f", fg="white")
        settings_menu.add_command(label="Change Key Bindings", command=self.change_key_bindings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        self.root.config(menu=menubar)

        # Style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", padding=6, font=("Helvetica", 12), background="#2e3f4f", foreground="white")
        style.configure("TButton", padding=6, font=("Helvetica", 12), background="#ff6666", foreground="white")
        style.configure("TEntry", padding=6, font=("Helvetica", 12))
        style.configure("TRadiobutton", font=("Helvetica", 12), background="#2e3f4f", foreground="white")
        style.map('TButton', background=[('active', '#ff4d4d')])

        ttk.Label(self.root, text="Click Interval (seconds):").pack(pady=10)
        self.interval_entry = ttk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, "1.0")

        self.click_type = tk.StringVar(value="click")
        ttk.Radiobutton(self.root, text="Auto Click", variable=self.click_type, value="click").pack(pady=5)
        ttk.Radiobutton(self.root, text="Hold Button", variable=self.click_type, value="hold").pack(pady=5)

        self.button_type = tk.StringVar(value="left")
        ttk.Radiobutton(self.root, text="Left Click", variable=self.button_type, value="left").pack(pady=5)
        ttk.Radiobutton(self.root, text="Right Click", variable=self.button_type, value="right").pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_action)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_action)
        self.stop_button.pack(pady=5)
        
        self.status_label = ttk.Label(self.root, text="Status: Stopped")
        self.status_label.pack(pady=10)

        self.key_bindings_label = ttk.Label(self.root, text=f"Start: {self.start_key}, Stop: {self.stop_key}")
        self.key_bindings_label.pack(pady=10)

    def start_action(self):
        try:
            self.delay = float(self.interval_entry.get())
            self.button = Button.left if self.button_type.get() == "left" else Button.right
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
            self.mouse.click(self.button, 1)
            time.sleep(self.delay)

    def holder(self):
        self.mouse.press(self.button)
        while self.holding:
            time.sleep(0.1)
        self.mouse.release(self.button)

    def setup_hotkeys(self):
        def on_press(key):
            try:
                if key.char == self.start_key:
                    self.start_action()
                elif key.char == self.stop_key:
                    self.stop_action()
            except AttributeError:
                pass

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def change_key_bindings(self):
        def save_key_bindings():
            new_start_key = start_key_entry.get()
            new_stop_key = stop_key_entry.get()
            if new_start_key and new_stop_key:
                self.start_key = new_start_key
                self.stop_key = new_stop_key
                self.key_bindings_label.config(text=f"Start: {self.start_key}, Stop: {self.stop_key}")
                key_binding_window.destroy()
            else:
                messagebox.showerror("Error", "Both key bindings must be set!")

        key_binding_window = tk.Toplevel(self.root)
        key_binding_window.title("Change Key Bindings")
        key_binding_window.geometry("300x280")
        key_binding_window.resizable(False, False)
        key_binding_window.configure(bg="#2e3f4f")

        key_binding_window.attributes("-topmost", True)
        key_binding_window.iconphoto(False, ImageTk.PhotoImage(Image.open(self.icon_path).resize((64, 64))))

        ttk.Label(key_binding_window, text="Start Key:").pack(pady=10)
        start_key_entry = ttk.Entry(key_binding_window)
        start_key_entry.pack(pady=5)
        start_key_entry.insert(0, self.start_key)

        ttk.Label(key_binding_window, text="Stop Key:").pack(pady=10)
        stop_key_entry = ttk.Entry(key_binding_window)
        stop_key_entry.pack(pady=5)
        stop_key_entry.insert(0, self.stop_key)

        save_button = ttk.Button(key_binding_window, text="Save", command=save_key_bindings)
        save_button.pack(pady=20)

    def on_closing(self):
        if messagebox.askyesno("Minimize to Tray", "Do you want to minimize to tray instead of exiting?"):
            self.hide_window()
        else:
            self.exit_app(None, None)

    def hide_window(self):
        self.root.withdraw()
        self.tray_icon.visible = True

    def show_window(self, icon, item):
        self.root.deiconify()
        self.tray_icon.visible = False

    def exit_app(self, icon, item):
        self.listener.stop()
        self.tray_icon.stop()
        self.root.destroy()

    def setup_tray_icon(self):
        image = Image.open(self.icon_path).resize((64, 64), Image.Resampling.LANCZOS)
        menu = (item('Show', self.show_window), item('Exit', self.exit_app))
        self.tray_icon = pystray.Icon("AutoClicker", image, "AutoClicker", menu)
        self.tray_icon.run_detached()

if __name__ == "__main__":
    icon_path = resource_path("src/autoclicklogo.png")
    root = tk.Tk()
    app = AutoClicker(root, icon_path)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()