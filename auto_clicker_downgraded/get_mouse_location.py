import pyautogui


def get_location_now():
    x, y = pyautogui.position()
    return x, y
