# %%
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
# %%
# 크롬 열기

reader = easyocr.Reader(['en'])
# subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

# 디버거 모드의 크롬 실행 경로 수정 (맥에서는 디폴트 설치 위치 사용)
subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', 
                  '--remote-debugging-port=9222', 
                  '--user-data-dir=/tmp/chrome_temp']) # 디버거 크롬 구동


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
# yes24 들어가기

driver.get(url='http://ticket.yes24.com/Perf/50431')
time.sleep(1)
driver.implicitly_wait(10)

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# %%
# 좌석 예약 클릭하기
driver.find_element(By.XPATH,'//*[@id="mainForm"]/div[10]/div/div[4]/a[4]').click()
time.sleep(0.5)
driver.implicitly_wait(10)

# %%
# 좌석 예약 창으로 변경
driver.switch_to.window(driver.window_handles[-1])
#driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="divFlash"]/iframe'))
driver.implicitly_wait(10)
# %%
driver.find_element(By.XPATH,'//*[@id="2024-10-12"]').click()
driver.find_element(By.XPATH,'//*[@id="btnSeatSelect"]').click()
# %%

#좌석 선택하기
print('******************************select seat')
driver.switch_to.window(driver.window_handles[-1])
driver.implicitly_wait(10)
driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="divFlash"]/iframe'))

#current_frame = driver.execute_script("return window.frameElement")
#print(current_frame)

driver.implicitly_wait(10)

# %%
def click_GradeRow():
    '''_summary_
    precondition : 프레임이 [@id="ifrmSeat"] 으로 되어있어야함
    Args: 0<=tr_num<n
    '''
    driver.find_elements(By.XPATH,'//*[@id="liLegend"]/div[2]/ul/li[1]').click()
    driver.implicitly_wait(10)
click_GradeRow
# %%
# 세부구역(GradeDetail) 클릭하기
def click_GradeDetail(li_num:int):
    '''_summary_
    precondition : 프레임이 [@id="ifrmSeat"] 으로 되어있어야함
    Args: 1<=li_num<n
    '''
    driver.find_element(By.XPATH,'//*[@id="grade_R석"]').click()
    driver.implicitly_wait(10)

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
