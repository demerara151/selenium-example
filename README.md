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

必要な環境が整っている方は、以下の内容を実行する必要はありません。あくまで確認のために書いてます

PowerShell を開いて、次のコマンドを打ちます

```powershell
winget install chrome
scoop install python poetry

# pip install selenium webdriver-manager
poetry add selenium webdriver-manager
```

> scoop の方の Chrome はバージョンの更新が遅れているため、winget でインストールしてます

poetry で 仮想環境を作成します

```powershell
poetry new web-scraper
cd web-scraper
poetry install
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
~\dev\repos\web-scraper > poetry shell

(web-scraper-py3.11)web-scraper > python --version
Python 3.11.1

(web-scraper-py3.11)web-scraper > pip show selenium
Name: selenium
Version: 4.7.2
Summary:
Home-page: https://www.selenium.dev
Author:
Author-email:
License: Apache 2.0
Location: C:\Users\User\dev\repos\web-scraper\.venv\Lib\site-packages
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

## FAQ

現在作成中

## LICENSE

MIT License

Copyright (c) <2022> <copyright demeraraonfire@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
