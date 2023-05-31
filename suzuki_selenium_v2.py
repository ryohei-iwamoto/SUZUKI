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
    current_handles = change_handle(current_handles)
    next_button2 = driver.find_element(By.XPATH, "//input[@id='nextButton2']")
    next_button2.click()
    time.sleep(1)
    # current_handles = change_handle(current_handles)
    # next_button3 = driver.find_element(By.XPATH, "//input[@name='btnNext']")
    # next_button3.click()
    # time.sleep(1)
    # current_handles = change_handle(current_handles)

    return current_handles


def select_car(count, current_handles):
    current_handles = change_handle(current_handles)
    if count == 0:
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table = soup.find_all('table')
        rows = table[1].find_all('tr')
        print(table)
        for row in rows:
            row_data = []
            cells = row.find_all('td')
            for cell in cells:
                spans = cell.find_all('span')
                for span in spans:
                    print(span.text)
                    row_data.append(span.text)
            car_list.append(row_data)
    
    car = driver.find_element(By.XPATH, f"//span[text()='{car_list[count][0]}']")
    car.click()
    next_button3 = driver.find_element(By.XPATH, "//input[@name='btnNext']")
    next_button3.click()
    time.sleep(1)
    return 0, current_handles


def select_car_models(count, current_handles):
    current_handles = change_handle(current_handles)

    if count == 0:
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table = soup.find_all('table')
        rows = table[2].find_all('tr')
        print(rows)
        for row in rows:
            row_data = []
            cells = row.find_all('td')
            for cell in cells:
                spans = cell.find_all('span')
                for span in spans:
                    row_data.append(span.text)
            car_model_list.append(row_data)

    car_model = driver.find_element(By.XPATH, f"//span[text()='{car_model_list[count][0]}']")
    car_model.click()

    print(car_model_list)
    next_button4 = driver.find_element(By.XPATH, "//input[@class='cmButton5']")
    print(next_button4)
    next_button4.click()
    time.sleep(1)
    return current_handles


def get_emo_handle(element):
    time.sleep(1)
    current_handles = driver.window_handles
    
    for current_handle in current_handles:
        driver.switch_to.window(current_handle)
        try:
            driver.find_element(By.XPATH, f"{element}")
            break
        except:
            pass
        
    time.sleep(2)

    current_handle = driver.current_window_handle
    current_handles.remove(menu_handle)
    current_handles.remove(current_handle)

    global genuinue_handle
    genuinue_handle = current_handles[0]
    return current_handles[0]



def select_big_emo():
    big_illusts = driver.find_elements(By.XPATH, "//img[@class='emoGrpIrtSelect']")
    for big_illust in big_illusts:
        big_illust.click()
    
    next_btn = driver.find_element(By.XPATH, "//input[@id='btnNext']")
    next_btn.click()

    return driver.window_handles


def select_small_emo():
    first_flag = 0

    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnNextImg"))
        )
        next_button = driver.find_element(By.ID, "btnNextImg")
        if first_flag != 0:
            try:
                driver.find_element_by_xpath('//*[@disabled="disabled" and @id="btnNextImg"]')
                break
            except:
                next_button.click()

        small_illusts = driver.find_elements(By.XPATH, "//img[@id='emoIlstNo']")
        for small_illust in small_illusts:
            small_illust.click()
        first_flag = 1
    
    next_btn = driver.find_element(By.XPATH, "//input[@id='btnNext']")
    next_btn.click()

    time.sleep(1)
    
    return driver.window_handles


def choose_handle(past_handles):
    handles = driver.window_handles
    print(handles)
    for past_handle in past_handles:
        handles.remove(past_handle)
    # driver.switch_to.window(handles[0])
    print(handles)
    return handles


def get_part_no(current_handle):
    driver.switch_to.window(genuinue_handle)
    source = driver.page_source
    print(source)
    
    del_btn = driver.find_element(By.XPATH, "//input[@id='btn_all_delete']")
    del_btn.click()

    alert = driver.switch_to.alert
    alert.accept()

    driver.switch_to.window(current_handle)


def choose_integra_parts(integra_handle, current_handle):
    print("!!!!!!!!!!!!!!!!!!!!!")
    driver.switch_to.window(integra_handle)

    rows = driver.find_elements(By.XPATH, "//tr[@id='tblRow']")
    print()

    for row in rows:
        row.click()
    
    ok_btn = driver.find_element(By.XPATH, "//input[@id='btnOk']")
    ok_btn.click()

    time.sleep(1)
    print(current_handle)
    
    driver.switch_to.window(current_handle)



def select_parts(current_handles, past_handles):
    print("################")
    print(menu_handle)
    print("#################")
    print(genuinue_handle)
    print("######################")

    current_handles.remove(menu_handle)
    current_handles.remove(genuinue_handle)
    print(current_handles)
    driver.switch_to.window(current_handles[0])
    
    first_flag = 0
    
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnNextFig"))
        )
        next_button = driver.find_element(By.ID, "btnNextFig")
        if first_flag != 0:
            try:
                print("!!!!!!!!!!!!")
                driver.find_element_by_xpath('//*[@disabled="disabled" and @id="btnNextFig"]')
                break
            except:
                print("$$$$$$$$$$$$$")
                next_button.click()

        parts_list = driver.find_elements(By.XPATH, "//tr[@id='listRow']")

        for i in range(len(parts_list)):
            parts = driver.find_elements(By.XPATH, "//tr[@id='listRow']")
            parts[i].click()
        #     for part in parts:
        #         if parts_list[i].text == part.text:
        #             part.click()
            new_handles = choose_handle(past_handles)
            # new_handles = driver.window_handles
            try:
                print(new_handles[1])
                choose_integra_parts(new_handles[1], driver.current_window_handle)
            except:
                pass
            time.sleep(1)
        
        get_part_no(driver.current_window_handle)
        first_flag = 1




def main():
    mouse_position()
    login()
    current_handles = before_car_select()
    car_model_count, current_handles = select_car(0, current_handles)
    current_handles = select_car_models(0, current_handles)
    genuinue_handle = get_emo_handle("/img[@class='emoGrpIrtSelect']")
    select_big_emo()
    current_handles= select_small_emo()
    current_handles = select_parts(current_handles, [genuinue_handle, menu_handle])


    







if __name__ == "__main__":
    main()