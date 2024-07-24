#%%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import subprocess
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import easyocr
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
driver.implicitly_wait(10)
# %%
# 인터파크로 들어가기
driver.get("https://tickets.interpark.com/goods/24007623")
time.sleep(1)
driver.implicitly_wait(10)

# %%
#driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
driver.implicitly_wait(10)

driver.find_element(By.XPATH, '//*[@id="productSide"]/div/div[2]/a[1]').click()
driver.implicitly_wait(10)

#%%
# 새로운 탭으로 이동
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
# driver.implicitly_wait(10)

# # 아이프레임으로 이동
# driver.implicitly_wait(10)
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

# %%
# 부정예매방지문자 OCR 생성

# 부정예매방지 문자 이미지 요소 선택
capchaPng = driver.find_element(By.XPATH,'//*[@id="imgCaptcha"]')
driver.implicitly_wait(10)

# 부정예매방지문자 입력
while capchaPng:
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

	# 입력이 잘 됐는지 확인하기
    display = driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]').is_displayed()
    # 입력 문자가 틀렸을 때 새로고침하여 다시입력
    if display:
        driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[1]/a[1]').click()
    # 입력 문자가 맞으면 select 함수 실행
    else:
        break
# %%
# 좌석 탐색
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
driver.implicitly_wait(10)

# 좌석등급 선택
driver.find_element(By.XPATH,'//*[@id="GradeRow"]/td[1]/div/span[2]').click()

while True:
    # 세부 구역 선택
    driver.find_element(By.XPATH,'//*[@id="GradeDetail"]/div/ul/li[1]/a').click()
    
    # 좌석선택 아이프레임으로 이동
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeatDetail"]'))
    
    # 좌석이 있으면 좌석 선택
    try:
        driver.find_element(By.XPATH,'//*[@id="Seats"]').click()
        # 결제 함수 실행
        break
        
    # 좌석이 없으면 다시 조회
    except:
        print('******************************다시선택')
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
        driver.find_element(By.XPATH,'/html/body/form[1]/div/div[1]/div[3]/div/p/a/img').click()
        time.sleep(1)
