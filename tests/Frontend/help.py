import pyautogui
import keyboard
import time

print("Press SPACE to get coordinates. Press ESC to exit.")

while True:
    if keyboard.is_pressed('space'):
        print(pyautogui.position())
        time.sleep(0.25)  # debounce

    if keyboard.is_pressed('esc'):
        print("Exiting...")
        break
