import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    import pyautogui
    import keyboard
    import time
    import random
    from configparser import ConfigParser
except ImportError as e:
    missing_package = str(e).split("'")[1]
    print(f"{missing_package} is not installed. Installing...")
    install_package(missing_package)

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
        print("text to type: ", text)
    return text

def type_text(text):
    words = text.split()
    for word in words:
        pyautogui.typewrite(word + ' ', interval=char_interval)
        time.sleep(random.uniform(min_interval, max_interval))

def main():
    done = True
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://play.typeracer.com/")

    while done:
        keyboard.wait("ctrl+alt+t")

        text_to_type = get_text_to_type(driver)
        done = False
        if text_to_type:
            type_text(text_to_type)

        done = True

main()