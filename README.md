# Selenium Example

Selenium の基本的な使い方と問題解決のための手引き

## 最新情報

Selenium v4.6.0 から実装された `Selenium Manager` ですが v4.11.0 からはドライバーどころかブラウザーまでも管理してくれるようになりました。

もはやブラウザーすら手動でインストールする必要がなくなり、各々のバージョンを気にする必要もなくなりました。

全ては `Chrome for Testing` が実装されたおかげです。通称 `CfT` は、Chrome が開発者のために作成した自動テスト専用のブラウザーです。普段使いを想定されていないため Chrome のダウンロードページには記載されていません。

このテストバージョンのブラウザーは、テストのために必要な最低限のファイルのみで構成されており、JSON 形式の API エンドポイントからダウンロード及びインストールが可能です。`Selenium Manager` がダウンロードやインストールを自動化し、ユーザーフォルダー直下の `~/.cache/selenium` 内に保管して管理します。以後、スクリプトを走らせるとはじめにこのキャッシュフォルダを確認し、存在していればそれを使い、なければ自動でダウンロードしてインストールされます。

### サンプルコード

```python
# バージョンの指定方法
from selenium import webdriver

options = webdriver.ChromeOptions()

# チャンネルによる指定
options.browser_version = "Stable"

# またはバージョンナンバーによる指定も可能
# options.browser_version = "115"

# あとはいつも通り
driver = webdriver.Chrome(options=options)
driver.get("https://books.toscrape.com/")
print(driver.title)
driver.quit()
```

サンプルコード：[using_manager.py](/src/using_manager.py)

チャンネルやバージョンナンバーを指定できることによりコードの再現性が高まります。環境による変化も最小限に抑えることができます。

## 前提

次の環境で実行しています。このリポジトリの内容は下記の環境を前提に話をしています

- Windows 11 home 23H2
- Python ^3.11
- Selenium ^4.11.0

以下の環境はオプションです。人によりけりです。好きなものを使ってください

- Windows のパッケージマネージャーは scoop を利用しています
- Python のパッケージマネージャーは poetry を利用しています
- エディターは VSCode です

## 仮想環境の構築

まず始めに仮想環境を構築します。私は poetry を利用していますが、各々好みのツールで仮想環境を初期化してください。

```powershell
poetry new automation-test
cd automation test
poetry add selenium
```

## 仮想環境の確認

仮想環境を有効化して、ライブラリのバージョンを確認します。

再度 poetry を使った場合の例を挙げます。各自の方法で仮想環境を有効化しバージョンを確認してください。

> 実際のところ poetry の場合は仮想環境を有効化しないでもインストールされているライブラリの詳細が確認できます。

```powershell
~\automation-test > poetry shell

~\automation-test > poetry run python --version
python 3.11.5

~\automation-test > poetry show --tree
selenium 4.13.0
├── certifi >=2021.10.8
├── trio >=0.17,<1.0
│   ├── attrs >=20.1.0
# 以下省略
```

ここで表示されるバージョンが、[前提](#前提)と合致しているか確認してください

## ユーザープロファイルの利用

`CfT` にはプロファイルがありません。そのため、プロファイルを利用したい場合は通常版の Chrome で利用しているプロファイルを指定する必要があります。

通常版の Chrome は `C:/Users/UserName/AppData/Local/Google/Chrome/User Data/` にプロファイルを格納しています。

```python
PROFILE = "C:/Users/UserName/AppData/Local/Google/Chrome/User Data/Profile 2"
options = webdriver.ChromeOptions()
options.add_argument(f"profile-directory={PROFILE}")
```

## 最小のコードで試運転

環境構築とバージョン確認が終わったので、最小のコードで問題なく動くか確認しましょう

このリポジトリの `src` フォルダにある [basic.py](./src/basic.py) をダウンロード、または内容をコピーして、自身の環境で実行してみてください

```powershell
# 仮想環境を有効化した状態で
poetry run python -m src.basic
```

このリポジトリそのものをクローンして頂いても結構です。

```powershell
git clone https://github.com/demerara151/selenium-example.git
cd selenium-example

# 仮想環境の初期化
poetry install

# 仮想環境のアクティベート
poetry shell

# poetry で Python スクリプトを実行する場合は以下のようにします
poetry run python -m src.basic

# また、エディターは VSCode を利用しているので、プロジェクトフォルダを VSCode で開けば全ての恩恵が受けられます
code .
```

もし、これで動かないようであれば、上記の手順の中に問題がある可能性があります。再度確認してください

## Troubleshoot

上記のコードで問題なく動けば、そのまま問題なく使い続けられるはずです

しかしながら、上記のコードすら動かない場合もあります

その場合は、`src` フォルダの [troubleshoot.py](./src/troubleshoot.py) を編集して実行してみてください

全てのパスを任意の場所に細かく指定できます

加えて任意のファイルにログを出力できます。ログを眺めて問題がどこにあるのか特定しましょう

### Windows 10 問題

Windows 11 からセキュリティ機能の強化としてサンドボックスが導入されました。サンドボックスとは、通常の環境から完全に独立した全く同じ環境でプログラムを実行し問題がないか確認するための箱庭機能です。ここでプログラムを実行してウィルスに感染しても実際の環境には影響がありません。また、環境に起因してプログラムが動かないということがないかを試すのにも効果的です。

さて、このサンドボックス機能ですが Chrome v115 から標準で実装されることになりました。そして、Windows 10 にこの機能はありません。

> 実際には、使用している Windows 10 がハードウェアの条件を満たしていればサンドボックスを有効化できます。しかしながら、多くの Windows 10 マシーンはこの条件を満たせません。

ここで発生するのが Windows 10 サンドボックス問題です。Chrome は標準でサンドボックスを有効化してブラウザーを開こうとします。しかし、Windows 10 にはこの機能がないためブラウザーを開くことに失敗します。その際によく出力されるのが 「`DevToolsActivePort` ファイルが存在しません」というエラーです。

```txt
selenium.WebDriverException: unknown error: DevToolsActivePort file doesn't exist
```

解決方法は 2 つあります。1 つは Windows10 を Windows 11 にアップグレードすること。それが不可能な場合は、Chrome のサンドボックス機能が動かないように無効化します。

これは Chrome のオプションフラッグを利用することで達成できます。

```python
options = webdriver.ChromeOptions()

# サンドボックスの無効化
options.add_argument("no-sandbox")

# DevToolsActivePort ファイルを利用可能にするために必要なオプション
options.add_argument("remote-debugging-port=9222")
```

ただし、サンドボックス機能を無効化することは推奨されていません。初めにも述べましたがこの機能はセキュリティを強化するために導入されています。

chromedriver は非常に強力なツールで悪用されるとかなり危険です。公式の chromedriver の配布ページにも「本番環境ではどんな弊害が発生するかわからないため、必ずテスト環境で実行すること。」といったような注意書きがあるほどです。

この「テスト環境」を簡単に用意できるのが今回説明したサンドボックス機能です。出来る限り Windows 11 にアップグレードすることをおすすめします。

### チェックリスト

Selenium スクリプト実行時にエラーが発生した際のチェックリストです

- [ ] Python のバージョンは 3.8 以上か
- [ ] Selenium のバージョンは 4.11 以上か
- [ ] 仮想環境を利用していない場合、複数の Python がインストールされていないか。または古い使っていない Python が残っていないか
- [ ] オプションの指定方法は正しいか。selenium 3.x と 4.x では指定方法が大きく異なるので注意
- [ ] 裏で Chrome が動いていないか。クラッシュハンドラーのようなプロセスが動いてたりするので Chrome に関連してそうなタスクは全て停止しておく
- [ ] アンチウィルスソフトの常駐を一時的に止めてみる
- [ ] FireWall の設定でサードパーティー制のアプリによる通信をブロックしていないか。Chrome は許可されているか
- [ ] Windows 10 の場合、`--no-sandbox` で、Sandbox を無効化する
- [ ] Windows 10 の場合、`--remote-debugging-port=9222` のようにポートナンバーを指定する
- [ ] `--verbose --log-path=C:\logs\selenium.log` のように指定しログを取る

### Windows におけるパスの扱い

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

## Selenium を使う目的

大きく分けて 3 つあります。

1. ページのスクリーンショットを撮影する

   これはページそのものをキャプチャする必要があるため、`urllib` や `requests` といったモジュールでは達成できません。

2. スクレイピングを実行したいページに `iframe` が使われている

   通常のリクエストでは iframe で読み込まれるコンテンツは取得できません。別途 iframe として埋め込まれている URL を指定して取得する必要があります。

   Selenium を使えば簡単にフレームを切り替えることができるので便利です。

3. Web サイトの挙動を確認する

   これが最も大きな理由になるはずです。自身で作成したサイトが意図した通りに動いているかどうかを確かたい時こそ Selenium のような自動化テストツールが有効です。

## Selenium を使う理由

ここで質問です。あなたが Selenium を使う目的は何ですか？

上記の 3 つのうちのどれかに目的が合致していますか？していないのであれば、そもそも Selenium を使う必要はないでしょう。

Web スクレイピングだけが目的の場合 Selenium を使う理由はスクショか iframe 対策ぐらいのもです。静的な Web サイトであればサーバーにリクエストを投げて HTML を取得し、欲しい値が含まれている要素を探します。また、サイトの管理者が JSON レスポンスを返すような API を提供していれば、欲しい値が含まれている JSON を取得します。API が提供されているかどうかは、ブラウザーの開発者ツールのネットワークタブでも確認できます。

## 代替手段

Selenium を使うには多少なりとも HTML や CSS に関する知識が要求されます。気軽にスクレイピングを試してみようと思ったのに、環境構築で躓いたりセレクターの指定方法が難解で何度やっても要素が見つからなかったりするのはよくあることです。

そこで、より初心者フレンドリーで気軽にスクレイピングを試せる PlayWright を紹介します。

### PlayWright

PlayWright は Microsoft が開発しているオープンソースプロジェクトで、非同期リクエストにも対応しておりコンテキストマネージャーでドライバーを管理できます。各種ブラウザ用のドライバーのインストールもコマンド一つで終わり、ブラウザーを別途インストールする必要もありません。

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

更に PlayWright には、ページ内の要素を指定するとセレクターを表示してくれる機能まであります。いちいち自身で HTML や CSS を勉強する必要もありません。PlayWright が認識できるコードの形で要素のセレクターを提示してくれます。

`iframe` が埋め込まれたページもいちいちフレーム切り替えを行う必要はありません。自動でフレームを認識しフレーム内に指定された要素がないか探索してくれます。

### 現代的スクレイピング手法

スクレイピングといえば、[BeautifulSoup]、[Requests]、Selenium の 3 本柱みたいに紹介されることが多いですが、どれも現代的な手法とは言えません。soup による parse は非常に遅く、requests は非同期に対応しておらず http2 も使えません。同様に selenium も playwright に劣る面が多々あります

現代的なスクレイピング手法として効率的なライブラリは、[httpx] と [selectolax]、そして playwright です

ブラウザの自動操作ができないとスクレイピングできないようなサイトは、`playwright + selectolax`、そうでない場合は、`httpx + selectolax` または、`httpx + regex` が個人的にはおすすめです。ただし、リクエストが非同期である必要がないのであれば `requests` もまだまだ現役です

ブラウザの自動操作だけが目的なら、そもそも Python である必要すらないかもしれません。GitHub で `automation` というキーワードで検索すると様々なプロジェクトが出てきます

<https://github.com/topics/automation>

## まとめ

自分の目的に適したツールを選びましょう

<!-- automation tool -->

[scrapy]: https://scrapy.org/
[cypress]: https://github.com/cypress-io/cypress
[playwright]: https://github.com/microsoft/playwright

<!-- scraping tool -->

[requests]: https://github.com/psf/requests
[httpx]: https://github.com/encode/httpx/
[selectolax]: https://github.com/rushter/selectolax
[beautifulsoup]: https://pypi.org/project/beautifulsoup4/

## LICENSE

This project is licensed under the terms of the [MIT license](./LICENSE).
