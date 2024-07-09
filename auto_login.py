# %%
# 크롬 드라이버 설정하기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess

import time

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
## https://tickets.interpark.com/으로 이동
# 인터파크 티켓 페이지로 이동
driver.get("https://tickets.interpark.com/")

# 지정된 요소가 로드될 때까지 대기
driver.implicitly_wait(10)

# %%
## 이동 후 로그인 버튼 클릭 /
# TODO
# 잠시 보류
# 요소 클릭
# time.sleep(1)
# login_btn = driver.find_element(By.XPATH, '//*[@title="로그인"]/a')
# print(login_btn)
# driver.execute_script("arguments[0].click();", login_btn)


# %%
