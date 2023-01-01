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
CHROME_DRIVER: str = "C:\\Users\\User\\bin\\chromedriver\\chromedriver.exe"

# ログの保存先
LOG_PATH: str = "C:\\Users\\User\\logs\\chrome.log"

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
url: str = "https://python.org"

# timeout = 10 seconds
driver.implicitly_wait(10)

driver.get(url)

window_title = driver.title
print(window_title)

# ドライバーを終了する
driver.quit()
