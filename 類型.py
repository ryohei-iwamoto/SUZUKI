import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.keys import Keys
import pandas as pd
import winsound



########################################################################################
# 設定
########################################################################################
driver_path = "C:\\Users\\NEC-USER10\\Downloads\\selenium-20230526T103825Z-001\\selenium\\chromedriver_win32\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--ignore-certificate-errors')

sub_list = []
car_model_list = []
menu_handle=0
genuinue_handle = 0
fig_handle = 0

dialog_image_path = './img/dialog_img.png'
ok_button_image_path = './img/ok_img.png'

############################
username = "EBW0063768H"
password = "57110TTAJ92"
############################

driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
driver.get("https://stn.suzuki.co.jp/sios/menu/SLMA_Menu.jsp")


##############################################################
# 証明書選択のポップアップはサイトではなくos側から出されているものなので switch.to_alertでは対応できない
##############################################################
def mouse_position():
    position = pyautogui.position()
    print("カーソルを一瞬だけ右上に持ってきてください。")
    print(position)
    while (position[0] < 1200 or position[1] > 50 ):
        # 現在のカーソルの位置を取得する
        position = pyautogui.position()
        print(position)


def ssl_pyauto_click():
    time.sleep(3)
    dialog_position = pyautogui.locateOnScreen(dialog_image_path)
    if dialog_position is not None:
        dialog_region = pyautogui.screenshot(region=dialog_position)
        ok_button_position = pyautogui.locateOnScreen(ok_button_image_path, grayscale=True, region=dialog_region)
        if ok_button_position is not None:
            ok_button_x = dialog_position.left + ok_button_position.left + ok_button_position.width // 2
            ok_button_y = dialog_position.top + ok_button_position.top + ok_button_position.height // 2
            pyautogui.click(ok_button_x, ok_button_y)
        else:
            print("not ok")
    else:
        print("not dialog")


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
    # print("###############################")
    # print(current_handles)
    # print(window)
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    diff_handles = list(set(window) - set(current_handles))
    driver.switch_to.window(diff_handles[0])
    
    return window

def before_car_select():
    time.sleep(1)
    # current_handles = driver.window_handles
    # current_handles = change_handle(current_handles)
    # time.sleep(1)
    current_handles = driver.window_handles
    try:
        driver.switch_to.window(menu_handle)
    except:
        pass
    
    parts_btn = driver.find_element(By.XPATH, "//img[@src='img/EPC.jpg']")
    parts_btn.click()
    time.sleep(3)
    current_handles = change_handle(current_handles)
    search_car_model_btn = driver.find_element(By.XPATH, "//input[@id='optRadio' and @value='2']")
    search_car_model_btn.click()
    time.sleep(1)
    ok_button = driver.find_element(By.XPATH, "//input[@id='nextButton']")
    ok_button.click()
    time.sleep(1)

    search_ruikata = driver.find_element(By.XPATH, "//input[@id='optRadio2' and @value='2']")

    search_ruikata.click()


    return current_handles


def send_ruikata(rui, kata):
    katasiki = driver.find_element(By.XPATH, "//input[@id='tmpKatashikiNo']")
    katasiki.send_keys(kata)
    
    ruibetu = driver.find_element(By.XPATH, "//input[@id='tmpRubetKubun']")
    ruibetu.send_keys(rui)
    ruibetu.send_keys(Keys.ENTER)
    


def select_car(count, current_handles, first=False):
    current_handles = change_handle(current_handles)
    if count == 0:
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table = soup.find_all('table')
        rows = table[1].find_all('tr')
        for row in rows:
            row_data = []
            cells = row.find_all('td')
            for cell in cells:
                spans = cell.find_all('span')
                for span in spans:
                    row_data.append(span.text)
            sub_list.append(row_data)
            
    car_row = driver.find_element(By.XPATH, f"//span[@id='syasyuNm' and text()='{sub_list[count][0]}']")
    car_row.click()
    next_button3 = driver.find_element(By.XPATH, "//input[@name='btnNext']")
    next_button3.click()
    time.sleep(1)
    return current_handles


def select_car_models(count, current_handles):
    time.sleep(1)
    current_handles = change_handle(current_handles)

    if count == 0:
        global car_model_list
        car_model_list = []
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table = soup.find_all('table')
        rows = table[2].find_all('tr')
        for row in rows:
            row_data = []
            cells = row.find_all('td')
            for cell in cells:
                spans = cell.find_all('span')
                for span in spans:
                    row_data.append(span.text)
            car_model_list.append(row_data)
    
    current_handles = driver.window_handles
    car_model = driver.find_element(By.XPATH, f"//span[@id='kisyuCd' and text()='{car_model_list[count][7]}']")
    car_model.click()

    next_button4 = driver.find_element(By.XPATH, "//input[@class='cmButton5']")
    next_button4.click()
    time.sleep(1)
    return current_handles, car_model_list[count]


def get_emo_handle(element):
    time.sleep(3)
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


def select_hojyo(count, current_handles):
    current_handles = change_handle(current_handles)
    time.sleep(1)
    if count == 0:
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table = soup.find_all('table')[0]
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            row_data = []
            cells = row.find_all('td')
            for cell in cells:
                inputs = cell.find_all('input')
                for input in inputs:
                    row_data.append(input['value'])
            sub_list.append(row_data)
    
    car_row = driver.find_element(By.XPATH, f"//input[@id='hojyoCd' and @value='{sub_list[count][0]}']")
    car_row.click()
    next_button3 = driver.find_element(By.XPATH, "//input[@id='nexter']")
    next_button3.click()
    time.sleep(1)
    return current_handles, sub_list[count], sub_list



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
                # driver.find_element_by_xpath('//*[@disabled="disabled" and @id="btnNextImg"]')
                driver.find_element(By.XPATH,'//*[@disabled="disabled" and @id="btnNextImg"]')
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
    for past_handle in past_handles:
        handles.remove(past_handle)
    # driver.switch_to.window(handles[0])
    return handles


def get_part_no(current_handle ,car ,car_model ,count):
    driver.switch_to.window(genuinue_handle)
    source = driver.page_source
    
    del_btn = driver.find_element(By.XPATH, "//input[@id='btn_all_delete']")
    del_btn.click()

    alert = driver.switch_to.alert
    alert.accept()

    driver.switch_to.window(current_handle)
    
    if not os.path.exists(f'output/{car[0]}/{car_model[7]}/'):
        os.makedirs(f'output/{car[0]}/{car_model[7]}/')
    
    with open(f'output/{car[0]}/{car_model[7]}/{count}.html', 'w', encoding='utf-8') as file:
        file.write(source)


def choose_integra_parts(integra_handle, current_handle):
    time.sleep(1)
    #------------------ここでsleep入れないとエラーになる。waitを追加--------------------#
    driver.switch_to.window(integra_handle)

    rows = driver.find_elements(By.XPATH, "//tr[@id='tblRow']")

    for row in rows:
        row.click()
    
    time.sleep(1)
    ok_btn = driver.find_element(By.XPATH, "//input[@id='btnOk']")
    ok_btn.click()

    time.sleep(1)
    
    driver.switch_to.window(current_handle)


def error_process():
    driver.switch_to.window(genuinue_handle)
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    table = soup.find("table", id="tblSios010")
    last_row = table.find_all("tr")[-1]
    partno_span = last_row.find("span", id="figNo")
    text = partno_span.text
    
    current_handles = driver.window_handles
    search_btn = driver.find_element(By.XPATH, "//input[@id='btn_search']")
    search_btn.click()
    fig_btn = driver.find_element(By.XPATH, "//a[@class='figInput']")
    fig_btn.click()
    re_input_fig(text, current_handles)


def re_input_fig(flag_text, current_handles):
    change_handle(current_handles)
    
    time.sleep(1)
    
    rows = driver.find_elements(By.XPATH, "//tr[@class='TitleCellA']")
    click_flag = False
    fig_count = 100

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        text = tds[0].text
        if text == flag_text:
            click_flag = True
            row.click()
            fig_count = 1
            continue
        
        if click_flag and fig_count <= 29:
            fig_count += 1
            row.click()
        
        if fig_count == 31:
            last_selected_fig = text
        
    current_handles = driver.window_handles
    ok_fig_btn = driver.find_element(By.XPATH, "//input[@id='btnSentaku']")
    ok_fig_btn.click()
    
    change_handle(current_handles)
    time.sleep(1)




def select_parts(current_handles, past_handles, car, car_model):
    current_handles.remove(menu_handle)
    current_handles.remove(genuinue_handle)
    driver.switch_to.window(current_handles[0])
    
    first_flag = 0
    btn_count = 1
    
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnNextFig"))
        )
        next_button = driver.find_element(By.ID, "btnNextFig")
        if first_flag != 0:
            try:
                driver.find_element_by_xpath('//*[@disabled="disabled" and @id="btnNextFig"]')
                break
            except:
                next_button.click()
                time.sleep(1)
                


        parts_list = driver.find_elements(By.XPATH, "//tr[@id='listRow']")

        for i in range(len(parts_list)):
            try:
                parts = driver.find_elements(By.XPATH, "//tr[@id='listRow']")
            except:
                error_process()
                parts = driver.find_elements(By.XPATH, "//tr[@id='listRow']")
            time.sleep(0.5)
            parts[i].click()
            try:
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(1)
                parts[i].click()
                parts[i].click()
            except:
                pass
                
        #     for part in parts:
        #         if parts_list[i].text == part.text:
        #             part.click()
            new_handles = choose_handle(past_handles)
            # new_handles = driver.window_handles
            try:
                choose_integra_parts(new_handles[1], current_handles[0])
                time.sleep(2)
            except:
                pass
        
        get_part_no(driver.current_window_handle, car, car_model, btn_count)
        btn_count += 1
        first_flag = 1
        

def logout():
    driver.switch_to.window(genuinue_handle)
    
    logout_btn = driver.find_element(By.XPATH, "//a[@id='btnLogOut']")
    logout_btn.click()
    driver.switch_to.window(menu_handle)


def menu_logout():
    logout_btn = driver.find_element(By.XPATH, "//a[text()='ログアウト']")
    logout_btn.click()
    driver.switch_to.window(menu_handle)


def check_all_fig():
    print(1)
    # todo


def get_ruikata_list():
    df = pd.read_csv('./original_data/ruikata_list.csv', dtype=str)
    ruikata_list = df.values.tolist()
    return ruikata_list


def get_ruikata():
    df = pd.read_csv('./original_data/ruikata_list.csv', dtype=str)
    ruikata_list = df.values.tolist()
    return ruikata_list


def get_car_model():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title_element = soup.title
    if title_element:
        if title_element.string == "SUZUKI_SIOS004 収録車種一覧（２）":
            car_model_list = []
            table = soup.find_all('table')
            rows = table[2].find_all('tr')
            for row in rows:
                row_data = []
                cells = row.find_all('td')
                for cell in cells:
                    spans = cell.find_all('span')
                    for span in spans:
                        row_data.append(span.text)
                car_model_list.append(row_data)
            return True, car_model_list
        else:
            return False, None
    else:
        return False, None
    
def get_ruikata():
    time.sleep(1)
    sub_list = []
    driver.switch_to.window(driver.window_handles[-1])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title_element = soup.title
    if title_element:
        if title_element.string == "SUZUKI_SIOS005 型式類別車種選択":
            table = soup.find_all('table')[0]
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                row_data = []
                cells = row.find_all('td')
                for cell in cells:
                    inputs = cell.find_all('input')
                    for input in inputs:
                        row_data.append(input['value'])
                sub_list.append(row_data)
            return True, sub_list
        else:
            return False, None
    else:
        return False, None
        


    # current_handles = driver.window_handles
# car_model = driver.find_element(By.XPATH, f"//span[@id='kisyuCd' and text()='{car_model_list[count][7]}']")
# car_model.click()

# next_button4 = driver.find_element(By.XPATH, "//input[@class='cmButton5']")
# next_button4.click()
# time.sleep(1)
# return current_handles, car_model_list[count]


    # current_handles = change_handle(current_handles)
    # time.sleep(1)
    # if count == 0:
    #     source = driver.page_source
    #     soup = BeautifulSoup(source, 'html.parser')

    
    # car_row = driver.find_element(By.XPATH, f"//input[@id='hojyoCd' and @value='{sub_list[count][0]}']")
    # car_row.click()
    # next_button3 = driver.find_element(By.XPATH, "//input[@id='nexter']")
    # next_button3.click()
    # time.sleep(1)
    # return current_handles, sub_list[count], sub_list



def make_list(current_handles, ruibet, katasiki):
    current_handles = change_handle(current_handles)
    sub_count = 0
    car_model_count = 0
    
    # sub_tf, sub_list = get_ruikata()
    car_model_tf, car_model_list = get_car_model()
    sub_tf, sub_list = get_ruikata()
    
    if car_model_tf:
        for car_model in car_model_list:
            sub_count = 0
            print(car_model)
            winsound.Beep(440,200)
            if car_model_count != 0:
                before_car_select()
                current_handles = driver.window_handles
                send_ruikata(ruibet, katasiki)
                time.sleep(2)
                current_handles = change_handle(current_handles)
            

            # car_model_tr = driver.find_element(By.XPATH, f"//span[@id='kisyuCd' and text()='{car_model[7]}']")
            # car_model_tr = driver.find_element(By.XPATH, f"//tr[@class='TitleCellA' and @onclick='selectRow(0)']/td/span[@id='kisyuCd' and text()='{car_model[7]}']/parent::td/parent::tr")
            # tr_elements = driver.find_elements(By.TAG_NAME, "tr")
            # # 条件を満たすtr要素を見つけ、その要素をクリック
            # for tr in tr_elements:
            #     print(tr.text)
            #     print("!!!!!!!!!!!!!!!")
            #     print(tr.text[0])
            #     print("#################")
            #     tekiyouSpec = tr.find_element(By.XPATH, ".//span[@id='tekiyouSpec']").text
            #     kisyuCd = tr.find_element(By.XPATH, ".//span[@id='kisyuCd']").text
            #     if tekiyouSpec == car_model[0] and kisyuCd == car_model[7]:
            #         tr.click()
            #         break  

            tekiyouCd = driver.find_element(By.XPATH, f'//tr[contains(td/span[@id="kisyuCd"], "{car_model[7]}") and td/span[@id="tekiyouSpec" and contains(text(), "{car_model[0]}")]]')
            tekiyouCd.click()


            next_button4 = driver.find_element(By.XPATH, "//input[@class='cmButton5']")
            next_button4.click()

            tekiyouCd = None
            
            # change_handle(current_handles)
            # ハンドル切り替えを設定
            sub_tf, sub_list = get_ruikata()
            
            winsound.Beep(300, 100)
            print(sub_tf)
            if sub_tf:
                for count, sub in enumerate(sub_list):
                    print(sub)
                    if sub_count != 0:
                        before_car_select()
                        current_handles = driver.window_handles
                        send_ruikata(ruibet, katasiki)
                        time.sleep(2)
                        current_handles = change_handle(current_handles)
                        # car_model_tr = driver.find_element(By.XPATH, f"//span[@id='kisyuCd' and text()='{car_model[7]}']")
                        # car_model_tr.click()

                        # tr_elements = driver.find_elements(By.TAG_NAME, "tr")
                        # for tr in tr_elements:
                        #     tekiyouSpec = tr.find_element(By.XPATH, "//span[@id='tekiyouSpec']").text
                        #     kisyuCd = tr.find_element(By.XPATH, "//span[@id='kisyuCd']").text
                        #     if tekiyouSpec == car_model[0] and kisyuCd == car_model[7]:
                        #         tr.click()
                        #         break  
                        tekiyouCd = driver.find_element(By.XPATH, f'//tr[contains(td/span[@id="kisyuCd"], "{car_model[7]}") and td/span[@id="tekiyouSpec" and contains(text(), "{car_model[0]}")]]')
                        tekiyouCd.click()

                        next_button4 = driver.find_element(By.XPATH, "//input[@class='cmButton5']")
                        next_button4.click()

                        tekiyouCd = None

                        time.sleep(2)
                        current_handles = change_handle(current_handles)

                    #要修正
                    # handle = driver.window_handles[-1]
                    # driver.switch_to.window(handle)
                    # print(driver.page_source)
                    car_row = driver.find_element(By.XPATH, f"//input[@id='hojyoCd' and @value='{sub[0]}']")
                    # print("!!!!!!!!!!!!!!")
                    # print(car_row)
                    # print("$$$$$$$$$$$$$$$$$$$")
                    car_row.click()
                    next_button3 = driver.find_element(By.XPATH, "//input[@id='nexter']")
                    next_button3.click()

                    genuinue_handle = get_emo_handle("/img[@class='emoGrpIrtSelect']")
                    select_big_emo()
                    current_handles = select_small_emo()
                    current_handles = select_parts(current_handles, [genuinue_handle, menu_handle], car_model, sub)
                    
                    logout()

                    sub_count += 1
                sub_count = 0
            else:
                genuinue_handle = get_emo_handle("/img[@class='emoGrpIrtSelect']")
                select_big_emo()
                current_handles = select_small_emo()
                current_handles = select_parts(current_handles, [genuinue_handle, menu_handle], car_model, sub)
                
                logout()

            car_model_count += 1



    elif sub_tf:
        sub_count = 0
        for sub in sub_list:
            if sub_count != 0:
                before_car_select()
                current_handles = driver.window_handles
                send_ruikata(ruibet, katasiki)
                time.sleep(2)
                current_handles = change_handle(current_handles)


            car_row = driver.find_element(By.XPATH, f"//input[@id='hojyoCd' and @value='{sub[0]}']")
            car_row.click()
            next_button3 = driver.find_element(By.XPATH, "//input[@id='nexter']")
            next_button3.click()

            genuinue_handle = get_emo_handle("/img[@class='emoGrpIrtSelect']")
            logout()
            sub_count += 1


    else:
        genuinue_handle = get_emo_handle("/img[@class='emoGrpIrtSelect']")
        select_big_emo()
        current_handles = select_small_emo()
        current_handles = select_parts(current_handles, [genuinue_handle, menu_handle], car_model, sub)
        
        logout()

        

    # タイトルがSUZUKI_SIOS005 型式類別車種選択のウィンドウが表示されたら
    # リストを上から取得
    
    # csvにして出力



def main():
    sub_count = 0
    car_model_count = 0
    car_first_flg = True
    
    mouse_position()
    login()
    ruikata_list = get_ruikata_list()
    

    for rui_kata in ruikata_list:
        before_car_select()
        
        current_handles = driver.window_handles
        
        try:
            send_ruikata(rui_kata[1], rui_kata[0])
            time.sleep(1)
            make_list(current_handles, rui_kata[1], rui_kata[0])
        except:
            time.sleep(1)
            menu_logout()


if __name__ == "__main__":
    main()