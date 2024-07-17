#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
import subprocess
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
#%%
# 크롬 열기
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
target_keyword = "두아 리파"

driver.get(url='https://tickets.interpark.com/')
driver.implicitly_wait(10)

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# %%
# 검색해서 이동하기
search = driver.find_element(By.XPATH,'//*[@id="__next"]/div/header/div/div[1]/div/div[1]/div[3]/div/input')
time.sleep(1)
driver.implicitly_wait(10)
time.sleep(1)
search.send_keys(target_keyword)
time.sleep(1)
search.send_keys(Keys.ENTER)
time.sleep(1)
driver.implicitly_wait(10)
contents = ['//*[@id="contents"]/div/div/div[2]/div[2]/a[1]', '//*[@id="contents"]/div/div/div[2]/div[2]/a']
target_content = '//*[@id="contents"]/div/div/div[2]/div[2]/a[1]'
if driver.findElement(By.xpath(target_content)).isDisplayed():
    
driver.find_element(By.XPATH,'//*[@id="contents"]/div/div/div[2]/div[2]/a[1]').click()
driver.implicitly_wait(10)

# %%
# 타이머 확인 확인하기

driver.execute_script('window.open("https://google.com");')
time.sleep(1)
driver.implicitly_wait(10)

# 타이머 확인 확인하기 - 새로 열린 탭으로 전환
driver.switch_to.window(driver.window_handles[-1])
time.sleep(1)
driver.implicitly_wait(10)

# 타이머 확인 확인하기 - 타이머 사이트 접속
url = "https://time.navyism.com/?host=ticket.interpark.com"
# 시간 동기화 사이트로 이동
driver.get(url)
driver.implicitly_wait(10)

# %%
# 서버시간 가져오는 함수
def get_server_time():
    # 서버 시간을 가져오는 함수
    time_element = driver.find_element(By.ID, "time_area")
    driver.implicitly_wait(2)
    # print(time_element.text)
    server_time_str = time_element.text  # "2024년 06월 19일 21:39:54.123" 형태로 시간 추출
    server_time = datetime.strptime(server_time_str.split('.')[0], "%Y년 %m월 %d일 %H시 %M분 %S초")
    return server_time

def wait_for_target_time(target_time):
    while True:
        current_time = get_server_time()
        # print(f"현재 서버 시간: {current_time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}", end="\t")
        # print(f"목표 서버 시간: {target_time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}", end="\t")
        # print((current_time >= target_time))
        if current_time >= target_time:
            break
        time.sleep(1)  # 0.1초 간격으로 체크
print(get_server_time())

# %%
# 목표 시간 설정 (예: 14:00:00)
TARGET_TIME_STR = "2024년 07월 17일 20시 57분 58초"
TARGET_TIME = datetime.strptime(TARGET_TIME_STR, "%Y년 %m월 %d일 %H시 %M분 %S초")
wait_for_target_time(TARGET_TIME)

# 목표 시간이 되면 팝업 띄우기
# driver.execute_script('alert("목표 시간이 되었습니다!");')

# # 팝업을 사용자가 확인할 때까지 대기
# WebDriverWait(driver, 30).until(EC.alert_is_present())
# alert = driver.switch_to.alert
# alert.accept()

print("목표 시간이 되었습니다!")
# %%
# 탭을 인터파크로 변경
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
driver.implicitly_wait(10)
driver.find_element(By.XPATH, '//*[@id="productSide"]/div/div[2]/a[1]').click()

# %%
