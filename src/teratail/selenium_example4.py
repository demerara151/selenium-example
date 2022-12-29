# type: ignore
"""プロファイルを指定して起動したいがそもそも起動しない"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# ユーザープロファイルの保管場所
PROFILE_PATH: str = (
    "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data"
)
# プロファイルの名前
PROFILE_DIR: str = "Default"

# Chrome 専用のオプション
options = webdriver.ChromeOptions()

options.add_argument(f"user-data-dir={PROFILE_PATH}")
options.add_argument(f"profile-directory={PROFILE_DIR}")

service = Service(
    # chromedriver のパス
    executable_path="chromedriver.exe",
)

# ドライバーの作成
try:
    driver = webdriver.Chrome(service=service, options=options)

except Exception as e:
    print(f"[Error]: {e}")
    raise

else:
    driver.get("https://www.youtube.com/")

    time.sleep(5)

    print(driver.title)

    time.sleep(5)

    driver.quit()
