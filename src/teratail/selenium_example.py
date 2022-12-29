# type: ignore
"""Google Colaboratoryでの不具合"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# URL関連
url: str = "https://maonline.jp/db/database"
login: str = "***.ac.jp"
password: str = "pwd"

# ヘッドレスモードの設定。
# True => ブラウザを描写しない。
# False => ブラウザを描写する。
options = webdriver.ChromeOptions()
options.add_argument("headless")

# Chromeを起動 # ここが問題
driver = webdriver.Chrome(
    executable_path="/content/chromedriver.exe", options=options
)

# ログインページを開く
driver.get(url)

# ログオン処理
# ユーザー名入力
driver.find_element("id", "username").send_keys(login)
driver.find_element("id", "btnNext").send_keys(Keys.ENTER)

# ブラウザの描写が完了するまで待機
driver.implicitly_wait(3)

# パスワード入力
driver.find_element("id", "passwd").send_keys(password)
driver.find_element("id", "btnSubmit").send_keys(Keys.ENTER)

# ログイン後のトップページを表示
print(driver.find_element("id", "username").text)

# ドライバーをクローズ
driver.quit()
