# type: ignore
"""Basic example of browser automation with selenium"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def get_window_title():

    # chromedriver のインストール
    # Reference: https://github.com/SergeyPirogov/webdriver_manager
    service = ChromeService(
        executable_path=ChromeDriverManager().install(),
    )

    # オプションの作成
    options = webdriver.ChromeOptions()

    # オプションの追加（先頭の -- は不要）
    # フルスクリーンでブラウザを開く
    options.add_argument("start-maximized")

    # 試験的オプションの追加
    # ドライバーが閉じたあともブラウザを開いたままにする
    # options.add_experimental_option("detach", True)

    # ドライバーの作成
    driver = webdriver.Chrome(service=service, options=options)

    # ページロード終了時すぐに要素が見つからない場合に見つかるまで待機する時間の設定
    driver.implicitly_wait(10)

    # 現在のブラウザのセッションで Web ページを読み込む
    driver.get("https://docs.python.org/ja/3/")

    # ページの要素を取得する
    page_title = driver.title

    # ページのタイトルがコンソールに表示されれば成功
    print(f"Page title is: {page_title}")

    # ドライバーを終了する
    driver.quit()


if __name__ == "__main__":
    get_window_title()
