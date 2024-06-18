# AutoClicker
--------

![AutoClickerLogo](https://www.marc-os.com/src/autoclicklogo.webp)

## Overview
--------

AutoClicker is a simple, user-friendly application designed to automate mouse clicks. It allows users to specify the click interval, choose between left and right mouse clicks, and decide whether to perform continuous clicks or hold the mouse button down. The application also features customizable hotkeys for starting and stopping the auto-clicking action.

## Installation
------------

### Requirements

-   Python 3.x
-   Required Python packages (listed in `requirements.txt`):
    -   `tkinter`
    -   `pynput`
    -   `Pillow`
    -   `pystray`
    -   `pyinstaller`

### Steps

1.  **Clone the Repository**:

    ```sh
    git clone https://github.com/mmrmagno/autoclicker.git
    cd autoclicker
    ```

2.  **Install the Required Packages**:

    ```sh
    pip install -r requirements.txt
    ```

3.  **Run the Application**:

    ```sh
    python auto.py
    ```

### Creating an Executable (Optional)

To use the application as a standalone executable, you can use PyInstaller.

1.  **Create the Executable**: For Windows:

    ```cmd
    python -m PyInstaller --onefile --windowed --add-data "src\\autoclicklogo.png;src" --icon=src\\autoclicklogo.png auto.py
    ```

    For Linux-based systems:

    ```sh
    python -m PyInstaller --onefile --windowed --add-data "src/autoclicklogo.png:src" --icon=src/autoclicklogo.png auto.py
    ```

2.  **Distribute the Executable**: The executable will be located in the `dist` directory. You can share this file with others.

## Usage
-----

### Main Window

1.  **Click Interval**: Set the interval between each click in seconds.
2.  **Click Type**: Choose between "Auto Click" for continuous clicks and "Hold Button" for holding the mouse button down.
3.  **Button Type**: Select either "Left Click" or "Right Click".
4.  **Start Button**: Start the auto-clicking action.
5.  **Stop Button**: Stop the auto-clicking action.
6.  **Status Label**: Displays the current status (Running or Stopped).
7.  **Key Bindings Label**: Shows the current hotkeys for starting and stopping the auto-clicking action.

### Settings Menu

1.  **Change Key Bindings**: Open a window to change the hotkeys for starting and stopping the auto-clicking action.

### System Tray

1.  **Minimize to Tray**: When the main window is closed, the application minimizes to the system tray.
2.  **Restore**: Restore the application from the system tray.
3.  **Exit**: Exit the application from the system tray.

## Hotkeys
-------

-   **Start Key**: Default is 's'. Press this key to start the auto-clicking action.
-   **Stop Key**: Default is 'x'. Press this key to stop the auto-clicking action.

### Changing Hotkeys

1.  Open the "Settings" menu.
2.  Select "Change Key Bindings".
3.  Enter the new start and stop keys and click "Save".

## Development
-----------

### Key Functions

-   `resource_path(relative_path)`: Returns the absolute path to a resource.
-   `AutoClicker`: Main class for the auto-clicker application.
    -   `__init__(self, root, icon_path)`: Initializes the application.
    -   `create_widgets(self)`: Creates and configures the main window widgets.
    -   `start_action(self)`: Starts the auto-clicking action.
    -   `stop_action(self)`: Stops the auto-clicking action.
    -   `clicker(self)`: Performs the auto-clicking.
    -   `holder(self)`: Holds the mouse button down.
    -   `setup_hotkeys(self)`: Sets up the hotkeys for starting and stopping the auto-clicking action.
    -   `change_key_bindings(self)`: Opens a window to change the hotkeys.
    -   `on_closing(self)`: Handles the window closing event.
    -   `hide_window(self)`: Minimizes the window to the system tray.
    -   `show_window(self, icon, item)`: Restores the window from the system tray.
    -   `exit_app(self, icon, item)`: Exits the application.
    -   `setup_tray_icon(self)`: Sets up the system tray icon and menu.


License
-------

This project is licensed under the MIT License. See the [LICENSE] file for details.

Support
-------

For support, please open an issue on the GitHub repository.AutoClicker Application Documentation
