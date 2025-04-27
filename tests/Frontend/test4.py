import pyautogui
import time
import os

# Setup folder
test_folder = os.path.join('test_screenshots', 'Test4')
os.makedirs(test_folder, exist_ok=True)

# Coordinates
textbox = (912, 404)
update_button = (1023, 405)
final_click = (966, 809)

# Test values
test_values = [
    'a',       # Letter
    '-100',    # Negative value
    '',        # Blank
    '1000',    # Positive integer
    '5000',
    '10000'
]

# Helper function
def click(x, y, delay=0.25):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)

# Run tests
for idx, value in enumerate(test_values):
    # Enter value
    click(*textbox)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(value)
    time.sleep(0.25)
    
    # Before screenshot
    pyautogui.screenshot(f'{test_folder}/before_{idx+1}_{value or "blank"}.png')
    
    # Click update button
    click(*update_button)
    time.sleep(0.5)
    
    # After screenshot
    pyautogui.screenshot(f'{test_folder}/after_{idx+1}_{value or "blank"}.png')
    time.sleep(0.5)

# Final click
click(*final_click)
