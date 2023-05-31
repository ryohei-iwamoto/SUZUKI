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
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


########################################################################################
# 設定
########################################################################################
# ChromeDriverのパスを設定する
# driver_path = "./chromedirver_win32/chromedriver.exe"
driver_path = "C:\sukuki\epc\selenium\chromedriver.exe"

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





cookies = driver.get_cookies()


# クッキーを辞書形式に変換
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}




certificate_file = './_.suzuki.co.jp.csv'  # 証明書ファイルのパスを指定


url = 'https://stn.suzuki.co.jp/sios/view/epc/sios001.html'
# リクエストヘッダにSSL証明書を指定
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers, cert=certificate_file,cookies=cookies_dict, verify=True)

# レスポンスをBeautifulSoupで解析
soup = BeautifulSoup(response.content, 'html.parser')



# ログイン後のクッキーを使用してリクエストを送信

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
# response = requests.get(url, headers=headers, cookies=cookies_dict)