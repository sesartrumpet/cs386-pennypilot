import pyautogui
import time
import os

coords = [
    (961, 530),  # Username textbox
    (963, 566),  # Password textbox
    (968, 779),  # Login button
    (1047, 605)  # Popup OK
]

test_sets = [
    ['', ''],                      # Empty set
    ['randomuser', 'randompass'],  # Fake data
    ['validuser', 'pass4']         # Real account (from Test1)
]

# Create Test2 folder
test_folder = os.path.join('test_screenshots', 'Test2')
os.makedirs(test_folder, exist_ok=True)

for idx, (username, password) in enumerate(test_sets):
    # Fill Username
    pyautogui.moveTo(coords[0])
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(username, interval=0.05)
    time.sleep(0.25)

    # Fill Password
    pyautogui.moveTo(coords[1])
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(password, interval=0.05)
    time.sleep(0.25)

    # Take before screenshot
    pyautogui.screenshot(f'{test_folder}/before{idx+1}.png')

    # Click Login button
    pyautogui.moveTo(coords[2])
    pyautogui.click()
    time.sleep(0.5)

    # Take after screenshot
    pyautogui.screenshot(f'{test_folder}/after{idx+1}.png')

    # Click popup OK
    pyautogui.moveTo(coords[3])
    pyautogui.click()
    time.sleep(0.5)
