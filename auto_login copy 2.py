#%%
import chromedriver_autoinstaller
from h11 import Data
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

import dataclasses 
import re
from datetime import datetime
# import pandas as pd
# import requests
#%%
# 크롬 열기

reader = easyocr.Reader(['en'])

# 디버거 모드의 크롬 실행 경로 수정 (맥에서는 디폴트 설치 위치 사용)
subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', 
                  '--remote-debugging-port=9222', 
                  '--user-data-dir=/tmp/chrome_temp']) # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# ChromeDriver 경로 설정
chrome_driver_path = "/opt/homebrew/bin/chromedriver"  # `which chromedriver`로 확인한 경로를 사용하세요

try:
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=option)
except Exception as e:
    print(f"ChromeDriver를 실행하는 데 실패했습니다: {e}")
    
# 브라우저 사이즈
driver.set_window_size(1900, 1000)
driver.implicitly_wait(10)
# %%
# 인터파크 들어가기

# driver.get(url='https://tickets.interpark.com/goods/24011164')
driver.get(url='https://tickets.interpark.com/goods/24012302')
time.sleep(1)
driver.implicitly_wait(10)

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# # 로그인 하기
# driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div/div[2]/a[1]').click()

# %%
## 빠르게 "예약하기" 누르기

# %%
## 예매하기 있는 버튼 값 가져오기 함수
# 해당 요소 찾기
@dataclasses.dataclass
class ButtonInfo:
    text:str
    data_check:bool
    
def get_button_info(css_selector:str)-> ButtonInfo:
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
    return ButtonInfo(
        text=element.text,
        data_check=element.get_attribute("data-check")
    )
button_info = get_button_info("#productSide > div > div.sideBtnWrap > a.sideBtn.is-primary")
# 요소의 텍스트 값 가져오기
print("요소의 텍스트 값:", button_info)

# %%
## 버튼 강제 변환
css_selector = "#productSide > div > div.sideBtnWrap > a.sideBtn.is-primary"
element = driver.find_element(By.CSS_SELECTOR, css_selector)
# class 속성 업데이트
current_class = element.get_attribute("class")
new_class = current_class.replace("is-disabled", "").strip()
driver.execute_script("arguments[0].setAttribute('class', arguments[1]);", element, new_class)
# data-check 속성 업데이트
driver.execute_script("arguments[0].setAttribute('data-check', 'false');", element)
# 버튼의 텍스트 변경
driver.execute_script("arguments[0].querySelector('span').textContent = '예매하기';", element)

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
import re
from datetime import datetime

def contains_pattern(text):
    """
    주어진 텍스트에 '남은시간 ' 패턴이 포함되어 있는지 확인합니다.
    
    :param text: 검사할 문자열
    :return: 패턴이 포함되어 있으면 True, 그렇지 않으면 False
    """
    pattern = r'남은시간 '
    return re.search(pattern, text) is not None

def extract_time_from_string(text)-> datetime:
    """
    주어진 텍스트에서 '남은시간 ' 뒤에 오는 시간을 추출하여 datetime 객체로 변환합니다.
    
    :param text: 시간 정보를 포함한 문자열
    :return: 추출된 시간을 datetime 객체로 변환한 결과, 패턴이 없으면 None
    """
    if not contains_pattern(text):
        return None
    
    # '남은시간 ' 뒤에 오는 시간을 추출하는 정규 표현식
    pattern = r'남은시간 (\d{2}:\d{2})'
    match = re.search(pattern, text)
    
    if match:
        # 추출된 시간 문자열을 가져옵니다.
        time_str = match.group(1)
        new_mm, new_ss = time_str.split(":")
        # 시간 문자열을 datetime 객체로 변환합니다.
        time_obj = datetime.strptime(time_str, '%M:%S')
        current_date = datetime.now()
        current_date.replace(minute=int(new_mm), second=int(new_ss))
        return current_date
    else:
        # 패턴이 일치하지 않는 경우 None을 반환합니다.
        return None

# %%
# 예제 사용
text = " 남은시간 19:03"
if contains_pattern(text):
    result = extract_time_from_string(text)
    if result:
        print(f"추출된 시간: {result.second}")
    else:
        print("시간 정보를 찾을 수 없습니다.")
else:
    print("패턴 '남은시간 '이 문자열에 포함되어 있지 않습니다.")


# %%

"""
    # 속성 출력
for attribute, value in attributes.items():
print(f"{attribute}: {value}")
"""