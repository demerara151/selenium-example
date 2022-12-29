# type:ignore
"""Chrome 起動時に特定の拡張機能が削除されてしまう現象"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("start-maximized")
chrome_options.add_argument(
    (
        "user-data-dir="
        "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data"
    )
)

chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(
    executable_path=(
        "C:\\Users\\User\\"
        "scoop\\apps\\chromedriver\\current\\chromedriver.exe"
    ),
    service_args=["--verbose"],
    log_path="C:\\Users\\User\\.logs\\chrome.log",
)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.python.org/")
