#%%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
#%%
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
#%%
url = "https://time.navyism.com/?host=ticket.interpark.com"
driver.get(url)

# %%
new_time = driver.execute_script(
    "return date('Y/m/d/H/i/s',time())"
)
print(new_time)
# %%
# Parse the HTML content using BeautifulSoup
soup = bs(response.content, 'html.parser')

# Find the element containing the server time
# The specific tag and class may need adjustment based on the website structure
time_element = soup.find('div', {'id': 'time_area'})  # Example selector
print(time_element)
# Extract and print the server time
#server_time = time_element.text if time_element else "Time not found"
#print("Interpark Server Time:", server_time)
# %%
new_time = driver.excute_script(
    "return_date('Y/m/d/H/i/s',time())"
)
print(now_time)