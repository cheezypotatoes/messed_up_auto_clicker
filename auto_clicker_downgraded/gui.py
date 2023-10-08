import tkinter as tk
from tkinter import ttk
import threading
from get_mouse_location import get_location_now
from start_auto_clicker import toggle_loop
import config


class ButtonsFrame(tk.Frame):
    def __init__(self, master=None, default_x=None, default_y=None):
        super().__init__(master)

        # Default keybind
        self.keybind = config.keybind_config

        # Condition of the app
        self.condition = "Inactive"

        # String for the status
        self.status_for_label = f"Status: {self.condition} | Keybind: {self.keybind}"

        # Default x and y (middle of the screen)
        self.x = default_x
        self.y = default_y

        # Grid row and column
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        # Button Style
        style = ttk.Style()
        style.configure("Cool.TButton",
                        padding=10,
                        font=("Helvetica", 12),
                        foreground="black")

        # Create a custom style for labels
        style = ttk.Style()
        style.configure("Cool.TLabel", padding=10,
                        font=("Helvetica", 12),
                        foreground="black")

        # Get location button
        self.get_location_button = ttk.Button(self,
                                              text="Get Location",
                                              style="Cool.TButton",
                                              command=self.get_location)
        self.get_location_button.grid(row=0,
                                      column=0,
                                      sticky="news")

        # Status Label
        self.status_label = ttk.Label(self,
                                      text=self.status_for_label,
                                      style="Cool.TLabel")
        self.status_label.grid(row=0,
                               column=1,
                               sticky="ns")


        # Location Coord
        self.coordinate_label = ttk.Label(self,
                                          text=f"Coordinates: x = {self.x}, y = {self.y}",
                                          style="Cool.TLabel")
        self.coordinate_label.grid(row=0,
                                   column=2,
                                   sticky="ns",
                                   pady=50)

    def get_location(self):
        # temporarily disable the buttons
        self.disable_all_buttons()
        # Change the label text first
        self.coordinate_label.config(text="Getting location in 5 seconds...")
        # Change status label temporarily
        self.status_label.config(text=f"Status: Getting Coordinates")
        # Schedule the actual work to be done after a delay
        self.after(5000, self.update_label_for_get_location)

    def update_label_for_get_location(self):
        # Get the x and y of the cord
        self.x, self.y = get_location_now()
        # Change the current coordinates
        self.coordinate_label.config(text=f"Coordinates: x = {self.x}, y = {self.y}")
        # Revert the status label to normal
        self.status_label.config(text=self.status_for_label)
        # Revert all button to active
        self.activate_all_buttons()

    def disable_all_buttons(self):
        # Disable all buttons
        self.get_location_button.config(state="disabled")

    def activate_all_buttons(self):
        # Enable all buttons
        self.get_location_button.config(state="activate")


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # Window Configure
        self.title("AutoClicker")
        self.geometry("800x200")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Get the middle of the screen
        self.middle_x = self.winfo_screenwidth() // 2
        self.middle_y = self.winfo_screenheight() // 2

        # Frame Instance
        self.frame_for_buttons = ButtonsFrame(default_x=self.middle_x, default_y=self.middle_y)
        self.frame_for_buttons.grid(row=0, column=0, sticky="nsew")

        # Toggle boolean
        self.autoclicker_toggle = False

        # Thread for key listener
        self.key_listener_thread = threading.Thread(target=self.starter)
        self.key_listener_thread.start()


    def starter(self):
        toggle_loop(self.middle_x, self.middle_y)


def main():
    window = MainWindow()
    window.mainloop()


if __name__ == "__main__":
    main()

