from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import time
import random

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

def type_text(text, min=0.01, max=0.015):
    words = text.split()
    for word in words:
        pyautogui.typewrite(word + ' ',interval=0.04)
        time.sleep(random.uniform(min,max))

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