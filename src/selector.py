"Example of CSS selectors."
from selectolax.parser import HTMLParser

html = """<div>
    <p class="message hello">Hello world</p>
    <a href="https://python.org">Python</a>
    <p class="message goodbye">Goodbye world</p>
    <a id="link" href="https://github.com">GitHub</a>
</div>
"""

tree = HTMLParser(html)

# タグでの指定
node = tree.css_first("div p")
message = node.text()
assert message == "Hello world"

# タグに合致する全ての要素
nodes = tree.css("div p")
messages = [node.text() for node in nodes]
assert messages == ["Hello world", "Goodbye world"]

# クラス名での指定
node = tree.css_first(".message")
message = node.text()
assert message == "Hello world"

# クラス名に合致する全ての要素
nodes = tree.css(".message")
messages = [node.text() for node in nodes]
assert messages == ["Hello world", "Goodbye world"]

# class="message goodbye": クラス名の中のスペースはドットで繋ぐ
node = tree.css_first(".message.goodbye")
message = node.text()
assert message == "Goodbye world"

# ID での指定
node = tree.css_first("#link")
link = node.text()
assert link == "GitHub"

# URL の抽出
# `.attributes` は辞書を返すので任意のキーでアクセスする
url = node.attributes["href"]
assert url == "https://github.com"


"""
Selenium の webdriver を使った場合も CSS の指定方法は同じ

# 要素単体の取得
element = driver.find_element(By.CSS_SELECTOR, ".message.goodbye")
message = element.text
assert message == "Goodbye world"

# 合致する全ての要素の取得
elements = driver.find_elements(By.CSS_SELECTOR, "div p")
messages = [element.text for element in elements]
assert messages == ["Hello world", "Goodbye world"]

# 属性の取得
element = driver.find_element(By.CSS_SELECTOR, "#link")
url = element.get_attribute("href")
assert url == "https://github.com"

"""

