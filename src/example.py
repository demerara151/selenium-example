# type: ignore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Chrome 本体の場所
PROGRAM_BINARY: str = (
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
)

# ユーザープロファイルの場所（わざと移動でもしない限り全員ここ）
USER_DATA_DIR: str = (
    "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data"
)

# 使いたいプロファイルの名前（任意）
PROFILE: str = "Profile 2"

# chromedriver の保管場所
CHROME_DRIVER: str = (
    "C:\\Users\\User\\scoop\\apps\\chromedriver\\current\\chromedriver.exe"
)

# ログの保存先
LOG_PATH: str = "C:\\Users\\User\\logs\\chrome.log"

# Web サイトで利用したい情報
USERNAME: str = "username"
PASSWORD: str = "password"

# オプションインスタンスの作成。selenium 4.0 以降は各ブラウザー専用のオプションを使う
options = webdriver.ChromeOptions()

# Chrome 本体の実行ファイルのパス
options.binary_location(PROGRAM_BINARY)

# ユーザープロファイルのパス。"User Data" を指定すれば自動的に "Default" を読み込む
options.add_argument(f"user-data-dir={USER_DATA_DIR}")

# 任意のユーザープロファイルの指定
options.add_argument(f"profile-directory={PROFILE}")

# 試験的オプションの追加
options.add_experimental_option("detach", True)

# サービスインスタンスの作成（executable_path 引数に chromedriver のパスを、log_path にログの保存先を指定）
service = Service(executable_path=CHROME_DRIVER, log_path=LOG_PATH)

# ドライバーの作成
driver = webdriver.Chrome(service=service, options=options)

# 指定した URL 先のページを読み込む
url: str = "https://teratail.com"
driver.get(url)

# HTML から任意の要素を取得
driver.find_element(
    "xpath", "/html/body/div/div[1]/header/div/div/a[2]"
).click()

# ページが描画されるまで待つ
driver.implicitly_wait(5)

username = driver.find_element(
    "xpath", "/html/body/div/div[1]/div/span[1]/input"
)
password = driver.find_element(
    "xpath", "/html/body/div/div[1]/div/span[2]/input"
)

# 任意の要素に任意の値を書き込む
username.send_keys(USERNAME)
username.send_keys(PASSWORD)

driver.find_element("xpath", "/html/body/div/div[1]/div/button").click()

driver.implicitly_wait(5)

# スクショを撮る
screenshot: bytes = driver.get_screenshot_as_png()

# 画像を保存する
with open("D:/Pictures/ScreenShot/ss.png", "wb") as f:
    f.write(screenshot)

# ドライバーを終了する
driver.quit()
