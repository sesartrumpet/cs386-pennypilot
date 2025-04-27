import pyautogui
import time
import os

# Folder to save screenshots (optional)
test_folder = os.path.join('test_screenshots', 'Test3')
os.makedirs(test_folder, exist_ok=True)

# UI element coordinates
dropdown_box = (964, 334)
already_saved_box = (967, 363)
date_box = (966, 394)
calculate_button = (968, 429)
error_popup_ok = (1059, 605)
confirm = (968, 835)

# Helper functions
def click(x, y, delay=0.25):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)

def press_enter_and_wait():
    pyautogui.press('enter')
    time.sleep(0.25)

def close_popup(step_name=''):
    click(*error_popup_ok)
    pyautogui.screenshot(f'{test_folder}/{step_name}_after_popup.png')

# === Test Phase 1: Dropdown ===
click(*dropdown_box)
press_enter_and_wait()  # Select first item

click(*calculate_button)
close_popup()

# Modify date
click(*date_box)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.write('4/27/26')  # Update year to 26
time.sleep(0.25)

click(*calculate_button)
time.sleep(0.25)

# Loop through remaining dropdown options
for _ in range(4):  # Adjust if more than 5 total values
    click(*dropdown_box)
    pyautogui.press('down')
    press_enter_and_wait()

    click(*calculate_button)
    time.sleep(0.25)

# === Test Phase 2: Already Saved Box ===
# Invalid: letter
click(*already_saved_box)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.write('a')
click(*calculate_button)
pyautogui.screenshot(f'{test_folder}/letter_error_before_popup.png')
close_popup('letter_error')


# Invalid: decimal
click(*already_saved_box)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.write('3.14')
click(*calculate_button)
pyautogui.screenshot(f'{test_folder}/decimal_error_before_popup.png')
close_popup('decimal_error')

# Valid: negative integer
click(*already_saved_box)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.write('-100')
click(*calculate_button)
time.sleep(0.25)

# Valid: positive integers
for value in ['1000', '5000', '10000']:
    click(*already_saved_box)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(value)
    click(*calculate_button)
    time.sleep(0.25)

# Final test: 0
click(*already_saved_box)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.write('0')
click(*calculate_button)
time.sleep(0.25)
# Final confirm click
click(*confirm)
