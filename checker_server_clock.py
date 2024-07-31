# %%
# 크롬 드라이버 설정하기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess

import time
from datetime import datetime

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
# 목표 시간 설정 (예: 14:00:00)
TARGET_TIME_STR = "2024년 06월 19일 21시 43분 54초"
TARGET_TIME = datetime.strptime(TARGET_TIME_STR, "%Y년 %m월 %d일 %H시 %M분 %S초")
# %%
# 시간 동기화 사이트로 이동
driver.get("https://time.navyism.com/?host=ticket.interpark.com")
driver.implicitly_wait(10)


# %%
def get_server_time():
    # 서버 시간을 가져오는 함수
    time_element = driver.find_element(By.ID, "time_area")
    print(time_element.text)
    # server_time_str = time_element.text  # "2024년 06월 19일 21:39:54.123" 형태로 시간 추출
    # server_time = datetime.strptime(server_time_str.split('.')[0], "%Y년 %m월 %d일 %H:%M:%S")
    # return server_time
print(get_server_time())
# %%
def wait_for_target_time(target_time):
    while True:
        current_time = get_server_time()
        print(f"현재 서버 시간: {current_time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}")
        if current_time >= target_time:
            break
        time.sleep(0.1)  # 0.1초 간격으로 체크

# %%
wait_for_target_time(TARGET_TIME)

# 목표 시간이 되면 팝업 띄우기
driver.execute_script('alert("목표 시간이 되었습니다!");')

# 팝업을 사용자가 확인할 때까지 대기
WebDriverWait(driver, 30).until(EC.alert_is_present())
alert = driver.switch_to.alert
alert.accept()



# %%
