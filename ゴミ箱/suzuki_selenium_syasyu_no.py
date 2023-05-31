import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



########################################################################################
# 設定
########################################################################################
driver_path = "C:\\Users\\NEC-USER10\\Downloads\\selenium-20230526T103825Z-001\\selenium\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--ignore-certificate-errors')

car_list = []
car_model_list = []
menu_handle=0
genuinue_handle = 0

############################
username = "EBW0063768H"
password = "57110TTAJ92"
############################

driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
driver.get("https://stn.suzuki.co.jp/sios/menu/SLMA_Menu.jsp")



def mouse_position():
    position = pyautogui.position()
    print("カーソルを一瞬だけ右上に持ってきてください。")
    print(position)
    while (position[0] < 1200 or position[1] > 50 ):
        # 現在のカーソルの位置を取得する
        position = pyautogui.position()
        print(position)


def login():
    username_field = driver.find_element(By.XPATH, "//input[@type='text']")
    username_field.send_keys(username)

    # password_field = driver.find_element(By.NAME, "J_password")
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.send_keys(password)

    submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit_button.click()
    time.sleep(1)
    global menu_handle
    menu_handle = driver.current_window_handle

def change_handle(current_handles):
    window = driver.window_handles
    for handle in window:
        for current_handle in current_handles:
            if handle != current_handle:
                driver.switch_to.window(handle)
                break
    
    return window

def before_car_select():
    time.sleep(1)
    current_handles = driver.window_handles
    current_handles = change_handle(current_handles)
    time.sleep(1)
    parts_btn = driver.find_element(By.XPATH, "//img[@src='img/EPC.jpg']")
    parts_btn.click()
    time.sleep(3)
    current_handles = change_handle(current_handles)
    search_car_model_btn = driver.find_element(By.XPATH, "//input[@value='2']")
    search_car_model_btn.click()
    time.sleep(1)
    ok_button = driver.find_element(By.XPATH, "//input[@id='nextButton']")
    ok_button.click()
    time.sleep(1)

    return current_handles


def main():
    mouse_position()
    login()
    current_handles = before_car_select()
    




if __name__ == "__main__":
    main()