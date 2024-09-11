import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    'selenium',
    'bs4',
    'pyautogui',
    'keyboard',
    'configparser'
]

# Ensure all required packages are installed
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} is not installed. Installing...")
        install_package(package)

# Now import all modules after ensuring they are installed
import pyautogui
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from configparser import ConfigParser
import time
import random

config = ConfigParser()
config.read('config.ini')

max_interval = config.get('Speed', 'max_interval').split('#')[0].strip()
min_interval = config.get('Speed', 'min_interval').split('#')[0].strip()
char_interval = config.get('Speed', 'char_interval').split('#')[0].strip()

try:
    max_interval = float(max_interval)
    min_interval = float(min_interval)
    char_interval = float(char_interval)
except ValueError as e:
    print(f"Error converting values to float: {e}")
    exit(1)

stop_typing = False

def stop_typing_keybind():
    global stop_typing
    stop_typing = True

keyboard.add_hotkey("ctrl+alt+s", stop_typing_keybind)

def get_text_to_type(driver):
    time.sleep(1)
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    span = soup.findAll("span")
    text = ""

    for i in span:
        if "unselectable" in str(i):
            text += i.text
            
    if not text:
        print("No text found")
        return None
    else:
        print("Text to type: ", text)
    return text

def type_text(text):
    global stop_typing
    words = text.split()
    stop_typing = False
    for word in words:
        if stop_typing:
            break
        pyautogui.typewrite(word + ' ', interval=char_interval)
        time.sleep(random.uniform(min_interval, max_interval))

def main():
    print("*** Close this window to stop the program.")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://play.typeracer.com/")

    while True:
            keyboard.wait("ctrl+alt+t")

            text_to_type = get_text_to_type(driver)
            
            if text_to_type:
                type_text(text_to_type)

if __name__ == "__main__":
    main()
