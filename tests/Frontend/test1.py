import pyautogui
import time
import os

# Coordinates
coords = [
    (969, 826),   # First C (click only once)
    (1029, 471),  # Username
    (1026, 504),  # Password
    (1023, 532),  # Confirm Password
    (1023, 564),  # First Name
    (1022, 599),  # Last Name
    (1022, 624),  # NAU Email
    (967, 782),   # Second-to-last C (click only)
    (1028, 605)   # Last C (click only)
]

# Test sets
test_sets = [
    ['', '', '', '', '', ''],  # All blank
    ['user1', 'pass1', 'wrongpass', 'John', 'Doe', 'jd1@nau.edu'],  # Password mismatch
    ['user2', 'pass2', 'pass2', 'Jane', 'Smith', 'js2@gmail.com'],  # Invalid email
    ['admin', 'pass3', 'pass3', 'Alex', 'Brown', 'ab3@nau.edu'],  # Username 'admin'
    ['validuser', 'pass4', 'pass4', 'Sam', 'Taylor', 'st4@nau.edu']  # Valid account
]

# Create Test1 folder
test_folder = os.path.join('test_screenshots', 'Test1')
os.makedirs(test_folder, exist_ok=True)

# First C (only once)
pyautogui.moveTo(coords[0])
pyautogui.click()
time.sleep(0.25)

# For each test set
for idx, texts in enumerate(test_sets):
    # Fill textboxes
    for (x, y), text in zip(coords[1:7], texts):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(text, interval=0.05)
        time.sleep(0.25)

    # Before screenshot
    pyautogui.screenshot(f'{test_folder}/before{idx+1}.png')

    # Second-to-last C click
    pyautogui.moveTo(coords[7])
    pyautogui.click()
    time.sleep(0.25)

    # After screenshot
    pyautogui.screenshot(f'{test_folder}/after{idx+1}.png')

    # Last C click
    pyautogui.moveTo(coords[8])
    pyautogui.click()
    time.sleep(0.25)
