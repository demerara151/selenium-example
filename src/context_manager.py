# type: ignore
"""Example of scraping using context manager with selenium manager"""
from selenium import webdriver
import asyncio
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from rich import print
from selectolax import parser
import httpx


@dataclass()
class ChromeBot:
    url: str
    timeout: float

    def extract_account_info(
        self, driver: webdriver.Chrome
    ) -> list[dict[str, str]]:
        "Extract account information from top page banner."
        driver.get(self.url)
        accounts = driver.find_elements(By.CSS_SELECTOR, ".postListBig li")
        return [
            {
                "name": account.find_element(
                    By.CSS_SELECTOR, ".accountName"
                ).text,
                "URL": account.find_element(
                    By.CSS_SELECTOR, "a"
                ).get_attribute("href"),
            }
            for account in accounts
        ]


@dataclass()
class Extractor:
    async def save_photo(self, database: list[dict[str, str]]) -> None:
        for i, account in enumerate(database):
            async with httpx.AsyncClient() as client:
                response = await client.get(account["URL"])
                tree = parser.HTMLParser(response.text)
                nodes = tree.css("figure img")
                for node in nodes:
                    img_url = node.attributes["src"]
                    response = await client.get(img_url)
                    photo = response.content
                    with open(f"{i:02}_{account['name']}.jpg", "wb") as f:
                        f.write(photo)


if __name__ == "__main__":
    URL: str = "https://instagrammernews.com/"
    instagram = ChromeBot(URL, 5.0)
    options = webdriver.ChromeOptions()
    options.add_argument("headless=new")

    with webdriver.Chrome(options) as driver:
        driver.implicitly_wait(instagram.timeout)
        accounts = instagram.extract_account_info(driver)
        print(accounts)

    extractor = Extractor()
    asyncio.run(extractor.save_photo(accounts))
