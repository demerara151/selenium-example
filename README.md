# Selenium Example

selenium の基本的な使い方と問題解決のための手引き

[teratail](https://terataile.com) 等の質問サイトで似たような質問がとても多いので自分自身の勉強のためにもリポジトリを作成しました

## 前提

次の環境で実行しています。このリポジトリの内容は下記の環境を前提に話をしています

-   Windows 11 home 22H2
-   Python 3.9 ~ 3.11.1 (できれば 3.10 が望ましい)
-   Selenium 4.6 ~ 4.7.2
-   Google Chrome Version 108.0.5359.125 (Official Build) (64-bit)
-   chromedriver 108.0.5359.75

以下の環境はオプションです。人によりけりです。好きなものを使ってください

-   Windows のパッケージマネージャーは winget と scoop の併用です
-   Python のパッケージマネージャーは poetry を利用しています
-   エディターは VSCode です

## 環境構築手順

私のやり方なので真似する必要はありません。このように構築した環境で実行していますということを明示するためです

> 必要な環境が整っている方は、以下の内容を実行する必要はありません

1. PowerShell を開いて、次のコマンドを打ちます

    ```powershell
    winget install chrome
    scoop install python poetry

    ```

    > scoop の方の Chrome はバージョンの更新が遅れているため、winget でインストールしてます

2. poetry で 仮想環境を作成します

    ```powershell
    poetry new chrome-automation
    cd chrome-automation
    poetry install
    ```

3. `webdriver-manager` をインストールします

    ```powershell
    # pip install selenium webdriver-manager
    poetry add selenium webdriver-manager
    ```

## Anaconda Navigator を利用している場合の注意点

デフォルトでインストールできる selenium のバージョンが 3.1 とかなので、インストール後にアップデートしておく必要があります

仮想環境をアクティベートした状態で、以下のコマンドを実行します

```powershell
conda activate <venv-name>
pip install -U selenium
```

## 環境の確認

`poetry shell` は、`venv activate` と同様の仮想環境のアクティベートコマンドです。各自の方法で仮想環境を有効にしてください

> 仮想環境を利用していない方は、`python --version` 以降を入力してください。とはいえ、今後のためにも仮想環境は作成しておいた方が何かと便利です

```powershell
~\dev\repos\chrome-automation > poetry shell

(chrome-automation-py3.11)chrome-automation > python --version
Python 3.11.1

(chrome-automation-py3.11)chrome-automation > pip show selenium
Name: selenium
Version: 4.7.2
Summary:
Home-page: https://www.selenium.dev
Author:
Author-email:
License: Apache 2.0
Location: C:\Users\User\dev\repos\chrome-automation\.venv\Lib\site-packages
Requires: certifi, trio, trio-websocket, urllib3
Required-by:
```

ここで表示されるバージョンが、[前提](#前提)と合致しているか確認してください

chromedriver を手動でインストールした場合、バイナリへのパスを通すか、バイナリが保存されているディレクトリで、次のコマンドを実行してください

```powershell
.\chromedriver.exe --version

ChromeDriver 108.0.5359.71 (1e0e3868ee06e91ad636a874420e3ca3ae3756ac-refs/branch-heads/5359@{#1016})
```

この場合、メジャーバージョンは 108 なので、これが Chrome のメジャーバージョンと一致しているか確認してください

Chrome のバージョンは、設定画面の `About Chrome` で確認できます。`Version 108.0.5359.125 (Official Build) (64-bit)` と表示されていれば、メジャーバージョンは 108 です

> `pip install webdriver-manager` をしている人はこのバージョン確認作業は不要です

## パスの確認

Selenium は chromedriver 以外のデフォルトのパスを自動で読み込んでくれます

以下の場所に該当するファイル、またはフォルダが存在しているか確認してください

-   Chrome 本体
    `C:\Program Files\Google\Chrome\Application\chrome.exe`

-   プロファイル
    `C:\Users\UserName\AppData\Local\Google\Chrome\User Data`

また、これ以外の場所に同一のファイルやフォルダがないかも確認してください。あれば削除してください

> 古くから Chrome を利用しており、長い間アンインストールして再インストールするといった作業を行っていない場合、`C:\Program Files (x86)` に、Chrome が保存されている場合があります。その場合は、別途コード内でパスを指定する必要があります

## ユーザープロファイルの利用

ユーザープロファイルを作成して selenium で読み込みたい場合、まず初めにコマンド引数で間違いなく該当のプロファイルが読み込めるか確認してください

```powershell
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' --profile-directory='Profile 2'
```

また、`C:\Users\UserName\AppData\Local\Google\Chrome\User Data` に該当のプロファイルが存在していることも合わせて確認してください。上記の場合は、`C:\Users\UserName\AppData\Local\Google\Chrome\User Data\Profile 2` です

## 最小のコードで試運転

環境構築とバージョン確認が終わったので、最小のコードで問題なく動くか確認しましょう

もし、これで動かないようであれば、上記の手順の中に問題がある可能性があります。再度確認してください

このリポジトリの `src` フォルダにある [basic.py](./src/basic.py) をダウンロード、または内容をコピーして、自身の環境で実行してみてください

リポジトリそのものをクローンして頂いても結構です。poetry を利用していれば環境構築はディレクトリの中で `poetry install` するだけで終わります

```powershell
git clone https://github.com/demerara151/selenium-example.git
cd selenium-example
poetry install
```

poetry で Python スクリプトを実行する場合は以下のようにします

```powershell
poetry run python -m src.basic.py
```

また、エディターは VSCode を利用しているので、プロジェクトフォルダを VSCode で開けば全ての恩恵が受けられます

```powershell
code .
```

## Troubleshoot

上記のコードで問題なく動けば、そのまま問題なく使い続けられるはずです

しかしながら、上記のコードすら動かない場合もあります

その場合は、`src` フォルダの [troubleshoot.py](./src/troubleshoot.py) を編集して実行してみてください

全てのパスを任意の場所に細かく指定できます

加えて任意のファイルにログを出力できます。ログを眺めて問題がどこにあるのか特定しましょう

## チェックリスト

Selenium でエラーが発生した際のチェックリスト

-   [ ] Python のバージョンは 3.7 以上か
-   [ ] Selenium のバージョンは 4.0 以上か
-   [ ] chromedriver のバージョンは Chrome のバージョンと一致しているか。または、`webdriver-manager` を利用しているか
-   [ ] 仮想環境を利用していない場合、複数の Python がインストールされていないか。または古い使っていない Python が残っていないか
-   [ ] パスは正しいか。コードで指定している引数を付けて、`chrome.exe` を `PowerShell` 等で実行しても問題なく実行できるか
-   [ ] オプションの指定方法は正しいか。selenium 3.x と 4.x では指定方法が大きく異なるので注意
-   [ ] 裏で Chrome が動いていないか。クラッシュハンドラーのようなプロセスが動いてたりするので Chrome に関連してそうなタスクは全て停止しておく
-   [ ] Chrome のクッキーとキャッシュを削除する
-   [ ] Chrome の 設定をリセットする
-   [ ] Chrome をアンインストールして再インストールする
-   [ ] アンチウィルスソフトの常駐を一時的に止めてみる
-   [ ] FireWall の設定でサードパーティー制のアプリによる通信をブロックしていないか。Chrome は許可されているか
-   [ ] `--remote-debugging-port=9222` のようにポートナンバーを指定する
-   [ ] Windows 10 の場合、`--no-sandbox` で、Sandbox を無効化する
-   [ ] `--verbose --log-path=C:\logs\selenium.log` のように指定しログを取る

## Windows におけるパスの扱い

一般的に Windows でパスを指定する場合はバックスラッシュ `\` を使いますが、Chrome はフォワードスラッシュ `/` でパスを指定しても認識してくれます（厳密に言うと PowerShell では通用するという話です）

```powershell
# パスは認識される
chrome.exe --user-data-dir='C:/Users/User/AppData/Local/Google/Chrome/User Data'
```

ただし、コマンドプロンプトを使う場合はその限りではありません。日本の Windows は、文字コードが特殊な Shift-JIS (932) で実行されています。フォワードスラッシュで構成されたパスは、文字コード UTF-8 (65001) に変更しないと認識してくれません。コマンドプロンプトでスクリプトを実行したい場合は、文字コードを事前に変更しておくか、Windows の設定を変更します

次のコマンドは、現在のセッションで使用される文字コードを UTF-8 に変更します

```cmd
chcp 65001
```

しかし、毎回これを打ってからスクリプトを実行するのはめんどうなので、次の手順で UTF-8 をどこでも使えるようにします

コントロールパネルを開きます。「時計と地域」->「地域」と進み、「管理」タブを開きます。「Unicode 対応ではないプログラムの言語」の「システムロケールの変更」をクリックします。そこに表示される「ベータ：ワールドワイド言語サポートで Unicode UTF-8 を使用」にチェックを入れます。適用、または OK をクリックし、PC を再起動します

以降、どこでフォワードスラッシュを使ってもパスを認識してくれるようになるはずです

## FAQ

現在作成中

## 代替手段

そもそも本当に Selenium が必要ですか？Selenium を使う目的はなんですか？スクレイピング？ブラウザの自動操作？

スクレイピングだけが目的の場合、Selenium を使う理由はほとんどありません。HTML を取得して、欲しい値が含まれている要素を探す (parse) か、API を叩いて情報 (json) を受け取ればいいだけです

ブラウザの自動操作をする目的はなんでしょう？自身のブラウザの挙動をテストしたいということなら他にもっと適したツールが沢山あります。中でも人気が高いのは、[Cypress] です

どうしても Selenium の挙動が必要なんだという場合は、[PlayWright] というライブラリもあります。こちらは非同期にも対応しておりコンテキストマネージャーでドライバーを管理できるので効率的です。各種ブラウザ用のドライバーのインストールもコマンド一つで終わります。スクリプトで `webdriver-manager` をインポートしたり引数にドライバーのパスを指定したりする必要もありません

<https://playwright.dev/python/docs/library>

```python
# playwright のコード例
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://playwright.dev")
    print(page.title())
    browser.close()
```

---

スクレイピングといえば、[BeautifulSoup]、[Requests]、Selenium の 3 本柱みたいに紹介されることが多いですが、どれも現代的な手法とは言えません。soup による parse は非常に遅く、requests は非同期に対応しておらず http2 も使えません。同様に selenium も playwright に劣る面が多々あります

現代的なスクレイピング手法として効率的なライブラリは、[httpx] と [selectolax]、そして playwright です

ブラウザの自動操作ができないとスクレイピングできないようなサイト(?)は、`playwright + selectolax`、そうでない場合は、`httpx + selectolax` または、`httpx + regex` が個人的にはおすすめです。ただし、リクエストが非同期である必要がないのであれば `requests` もまだまだ現役です

ブラウザの自動操作だけが目的なら、そもそも Python である必要すらないかもしれません。GitHub で `automation` というキーワードで検索すると様々なプロジェクトが出てきます

<https://github.com/topics/automation>

---

**まとめ**

自分の目的に適したツールを選びましょう

<!-- automation tool -->

[cypress]: https://github.com/cypress-io/cypress
[playwright]: https://github.com/microsoft/playwright

<!-- scraping tool -->

[requests]: https://github.com/psf/requests
[httpx]: https://github.com/encode/httpx/
[selectolax]: https://github.com/rushter/selectolax
[beautifulsoup]: https://pypi.org/project/beautifulsoup4/

## LICENSE

This project is licensed under the terms of the [MIT license](./LICENSE).
