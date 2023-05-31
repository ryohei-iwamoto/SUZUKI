# from selenium import webdriver
import time
import pyautogui
# from bs4 import BeautifulSoup
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import csv
# import re
# import os
# import openpyxl


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options





########################################################################################
# 設定
########################################################################################
# ChromeDriverのパスを設定する
# driver_path = "./chromedirver_win32/chromedriver.exe"
driver_path = "C:\\Users\\NEC-USER10\\Downloads\\selenium-20230526T103825Z-001\\selenium\\chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--ignore-certificate-errors')
# options.add_argument("--headless")

username = "EBW0063768H"
password = "57110TTAJ92"









# WebDriverを起動
driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
# driver = webdriver.Chrome(service=Service(driver_path), options=options)
# driver = webdriver.Chrome("./chromedirver_win32/chromedriver.exe")

# Googleのトップページにアクセスする例
driver.get("https://stn.suzuki.co.jp/sios/menu/SLMA_Menu.jsp")
# ok_button = driver.switch_to.alert
#ok_button.accept()


position = pyautogui.position()
print("カーソルを一瞬だけ右上に持ってきてください。")
print(position)
while (position[0] < 1200 or position[1] > 50 ):
    # 現在のカーソルの位置を取得する
    position = pyautogui.position()
    print(position)




# username_field = driver.find_element(By.NAME, "J_username")
username_field = driver.find_element(By.XPATH, "//input[@type='text']")
username_field.send_keys(username)

# password_field = driver.find_element(By.NAME, "J_password")
password_field = driver.find_element(By.XPATH, "//input[@type='password']")
password_field.send_keys(password)

submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
submit_button.click()



current_window_handle = driver.current_window_handle

parts_btn = driver.find_element(By.XPATH, "//img[@src='img/EPC.jpg']")
parts_btn.click()

time.sleep(3)
print("!!!!!!!!!!!!!!!!!!!!!!!!")

window_handles = driver.window_handles

for handle in window_handles:
    if handle != current_window_handle:
        driver.switch_to.window(handle)
        break


search_car_model_btn = driver.find_element(By.XPATH, "//input[@value='2']")
search_car_model_btn.click()

# ok_button = driver.find_element_by_id('nextButton')
ok_button = driver.find_element(By.XPATH, "//input[@id='nextButton']")
ok_button.click()

time.sleep(1)

current_window_handles = driver.window_handles

next_button2 = driver.find_element(By.XPATH, "//input[@id='nextButton2']")
next_button2.click()


value = driver.execute_script('returnarguments[0].value;', next_button2)


html = driver.page_source
print(html)
print("!!!!!!!!!")
print(value)


window_handles = driver.window_handles

for handle in window_handles:
    for current_window_handle in current_window_handles:
        if handle != current_window_handle:
            driver.switch_to.window(handle)
            break


current_window_handle = driver.current_window_handle

time.sleep(1)

next_button3 = driver.find_element(By.XPATH, "//input[@name='btnNext']")
print(next_button3)
next_button3.click()

window_handles = driver.window_handles

for handle in window_handles:
    if handle != current_window_handle:
        driver.switch_to.window(handle)
        break

current_window_handle = driver.current_window_handle


next_button4 = driver.find_element(By.XPATH, "//input[@input='btnNext']")
next_button4.click()

window_handles = driver.window_handles

for handle in window_handles:
    if handle != current_window_handle:
        driver.switch_to.window(handle)
        break


time.sleep(1111111)

# user_name = 


