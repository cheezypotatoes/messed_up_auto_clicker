import keyboard
import time
import config
import pyautogui

run_status = False
hotkey = config.keybind_config


def toggle_loop(x, y):
    loop_active = False

    def toggle():
        nonlocal loop_active
        loop_active = not loop_active
        global run_status
        run_status = loop_active

    keyboard.add_hotkey(hotkey, toggle)

    try:
        while True:
            if loop_active:
                # Put your loop code here
                pyautogui.moveTo(x, y)
                pyautogui.click()
            time.sleep(0.1)  # Adjust the sleep duration as needed

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up the keyboard library
        keyboard.unhook_all()
