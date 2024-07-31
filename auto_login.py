#%%
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from datetime import datetime
import subprocess
import time
import easyocr
# import pandas as pd
# import requests
#%%
# 크롬 열기

reader = easyocr.Reader(['en'])
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
# 브라우저 사이즈
driver.set_window_size(1900, 1000)
driver.implicitly_wait(10)
# %%
# 인터파크 들어가기

driver.get(url='https://tickets.interpark.com/goods/24007623')
time.sleep(1)
driver.implicitly_wait(10)

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# %%
# 좌석 예약 클릭하기
driver.find_element(By.XPATH,'//*[@id="productSide"]/div/div[2]/a[1]').click()
time.sleep(0.5)
driver.implicitly_wait(10)

# %%
# 좌석 예약 창으로 변경
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
driver.implicitly_wait(10)

# %%
# 캡챠 풀기
capchaPng = driver.find_element(By.XPATH,'//*[@id="imgCaptcha"]')

while capchaPng:
    print('---------------capcha')
    result = reader.readtext(capchaPng.screenshot_as_png, detail=0)
    capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '')\
        .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '')\
        .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')
        
    # 입력
    driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[3]').click()
    chapchaText = driver.find_element(By.XPATH,'//*[@id="txtCaptcha"]')
    chapchaText.send_keys(capchaValue)
        
    #입력완료 버튼 클릭
    driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]').click()

    display = driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]').is_displayed()
    if display:
        # 새로고침
        driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[1]/a[1]').click()
    else:
        break
# %%
# 좌석 선택하기
print('******************************select seat')
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))


# %%
# 구역(GradeRow) 클릭하기
def click_GradeRow(tr_num:int):
    '''_summary_
    precondition : 프레임이 [@id="ifrmSeat"] 으로 되어있어야함
    Args: 0<=tr_num<n
    '''
    driver.find_elements(By.XPATH,'//*[@id="GradeRow"]/td[1]/div/span[2]')[tr_num].click()
    driver.implicitly_wait(10)
click_GradeRow(tr_num=1)

# %%
# 세부구역(GradeDetail) 클릭하기
def click_GradeDetail(li_num:int):
    '''_summary_
    precondition : 프레임이 [@id="ifrmSeat"] 으로 되어있어야함
    Args: 1<=li_num<n
    '''
    driver.find_element(By.XPATH,f'//*[@id="GradeDetail"]/div/ul/li[{li_num}]/a').click()
    driver.implicitly_wait(10)
click_GradeDetail(li_num=1)

# %%
## 좌석선택하기
# try:
driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeatDetail"]'))
driver.implicitly_wait(10)
driver.find_element(By.XPATH,'//*[@id="Seats"]').click()
driver.implicitly_wait(10)
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
driver.find_element(By.XPATH,'//*[@id="NextStepImage"]').click()
driver.implicitly_wait(10)
# except:
#     print('******************************다시선택')
#     driver.switch_to.default_content()
#     driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
#     driver.find_element(By.XPATH,'/html/body/form[1]/div/div[1]/div[3]/div/p/a/img').click()
#     time.sleep(1)     

# %%
