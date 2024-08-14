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
# yes24 들어가기

driver.get(url='http://ticket.yes24.com/Perf/50431')
time.sleep(1)
driver.implicitly_wait(10)

driver.find_element(By.XPATH, '//*[@id="mainForm"]/div[10]/div/div[4]/a[4]').click()


# 예매하기 탭 이동
time.sleep(1)
print("--------------------")
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])

# 날짜 선택
driver.find_element(By.CLASS_NAME, "select").click()
driver.find_element(By.XPATH, '//*[@id="btnSeatSelect"]').click()

# 구역, 좌석 선택하기
driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="divFlash"]/iframe'))

driver.find_element(By.XPATH, '//*[@id="area0"]').click()

driver.implicitly_wait(30)

print("-----selection----")
#    By.XPATH, '//*[@id="divSeatArray"]/div[string-length(@title)>0]').click()
driver.find_element(By.XPATH, '//*[@id="t1800026"]').click()

driver.implicitly_wait(10)

# 좌석선택 완료
driver.find_element(
    By.XPATH, '//*[@id="form1"]/div[3]/div[2]/div/div[2]/p[2]/a/img'
).click()

driver.implicitly_wait(10)

# 할인/쿠폰
driver.switch_to.default_content()
driver.find_element(By.XPATH, '//*[@id="StepCtrlBtn03"]/a[2]/img').click()

driver.implicitly_wait(10)

# 수령방법
time.sleep(3)  ## 주문자 정보 받아오기``
driver.find_element(By.XPATH, '//*[@id="StepCtrlBtn04"]/a[2]/img').click()

driver.implicitly_wait(10)

# 결제방법
driver.find_element(By.XPATH, '//*[@id="rdoPays22"]').click()  # 무통장 입금

select = Select(driver.find_element(By.XPATH, '//*[@id="selBank"]'))
select.select_by_index(1)

driver.implicitly_wait(10)

# 예매하기
driver.find_element(By.XPATH, '//*[@id="cbxAllAgree"]').click()
driver.find_element(By.XPATH, '//*[@id="imgPayEnd"]').click()
