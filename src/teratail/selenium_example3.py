# type: ignore
"""ログインした状態で開きたいが、指定した URL への画面遷移が行われない"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

userDir: str = "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data"
profileDir: str = "Default"

options = webdriver.ChromeOptions()
options.binary_location(
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
)
options.add_argument("user-data-dir=" + userDir)
options.add_argument("profile-directory=" + profileDir)

service = Service(
    executable_path=(
        "C:\\Users\\User\\scoop\\apps\\"
        "chromedriver\\current\\chromedriver.exe"
    ),
)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.youtube.com/")

time.sleep(5)

driver.quit()
