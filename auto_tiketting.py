import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import easyocr



# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1900, 1000)
interpark_url = 'https://tickets.interpark.com//'


# 웹페이지가 로드될 때까지 2초를 대기
driver.implicitly_wait(time_to_wait=2)  
driver.get(url=interpark_url)


# 로그인
driver.find_element(By.LINK_TEXT,'로그인').click()
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
userId = driver.find_element(By.ID, 'userId')
userId.send_keys('아이디')
userPwd = driver.find_element(By.ID, "userPwd")
userPwd.send_keys('패스워드')
userPwd.send_keys(Keys.ENTER)


# 티켓 사이트 이동
search = driver.find_element(By.XPATH,'//*[@id="__next"]/div/header/div/div[1]/div/div[1]/div[3]/div/input')
search.send_keys('싸이 올나잇')
search.send_keys(Keys.ENTER)

driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div/div/div[1]/div[2]/a[1]/div[1]').click()


#예매하기
print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
driver.find_element(By.XPATH,'//*[@id="productSide"]/div/div[2]/a[1]').click()


print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))



# 좌석 탐색
def select():
    print('******************************select seat')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
    # 구역선택
    #driver.find_element(By.XPATH,'//*[@id="GradeRow"]/td[1]/div/span[2]').click()

    while True:
        # 세부구역 선택
        driver.find_element(By.XPATH,'//*[@id="GradeDetail"]/div/ul/li[1]/a').click()
        driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeatDetail"]'))
        try:
            driver.find_element(By.XPATH,'//*[@id="Seats"]').click()
            payment()
            break
        except:
            print('******************************다시선택')
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
            driver.find_element(By.XPATH,'/html/body/form[1]/div/div[1]/div[3]/div/p/a/img').click()
            time.sleep(1)     
    

def payment():
    print('******************************payment')
    #좌석선택
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
    driver.find_element(By.XPATH,'//*[@id="NextStepImage"]').click()

    #가격선택
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
    select = Select(driver.find_element(By.XPATH, '//*[@id="PriceRow001"]/td[3]/select'))
    select.select_by_index(1)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()

    #주문자 확인
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
    driver.find_element(By.XPATH,'//*[@id="YYMMDD"]').send_keys('생년월일')
    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()

    #결제
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmBookStep"]'))
    driver.find_element(By.XPATH,'//*[@id="Payment_22004"]/td/input').click()
            
    select2 = Select(driver.find_element(By.XPATH, '//*[@id="BankCode"]'))
    select2.select_by_index(1)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()
            
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmBookStep"]'))
    driver.find_element(By.XPATH,'//*[@id="checkAll"]').click()
    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="LargeNextBtnImage"]').click()



# 부정예매방지 문자
reader = easyocr.Reader(['en'])
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
        select()
        break