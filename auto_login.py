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
driver.implicitly_wait(10)
# %%
# 인터파크로 들어가기
driver.get("https://tickets.interpark.com/goods/24007623")
time.sleep(1)
driver.implicitly_wait(10)

# %%
# 타이머 확인 확인하기 - 새 탭을 열기 위해 자바스크립트 실행
driver.execute_script('window.open("https://google.com");')
time.sleep(1)
driver.implicitly_wait(10)

# %%
# 타이머 확인 확인하기 - 새로 열린 탭으로 전환
driver.switch_to.window(driver.window_handles[-1])
time.sleep(1)
driver.implicitly_wait(10)

# %%
# 타이머 확인 확인하기 - 타이머 사이트 접속
url = "https://time.navyism.com/?host=ticket.interpark.com"
driver.get(url)
time.sleep(1)
driver.implicitly_wait(10)

# %%
new_time = driver.execute_script(
    "return date('Y/m/d/H/i/s',time())"
)
print(new_time)
type(new_time)

#%%

while True:
    new_time = driver.execute_script(  
    "return date('Y/m/d/H/i/s',time())"
    )
    print(new_time)
    if new_time >= "2024/07/17/20/54/00":
        break
    else:
        time.sleep(0.5)

    
# %%
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
driver.implicitly_wait(10)

driver.find_element(By.XPATH, '//*[@id="productSide"]/div/div[2]/a[1]').click()
