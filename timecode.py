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

    