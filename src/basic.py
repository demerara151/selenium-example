"""Basic example of browser automation with selenium"""
from selenium import webdriver


def get_window_title() -> None:
    # オプションインスタンスの作成
    options = webdriver.ChromeOptions()

    # ブラウザーのバージョンを指定
    options.browser_version = "Stable"

    # ヘッドレスモードで開くオプションを追加（先頭の -- は不要）
    options.add_argument("headless=new")  # type: ignore

    # 試験的オプションの追加
    # ドライバーが閉じたあともブラウザを開いたままにする
    # options.add_experimental_option("detach", True)

    # ドライバーの作成
    driver = webdriver.Chrome(options=options)

    # ページ遷移終了時すぐに要素が見つからない場合に見つかるまでページロードを待機する時間の設定
    driver.implicitly_wait(5)

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

