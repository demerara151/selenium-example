# type: ignore
"""Example of scraping using context manager with selenium manager"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from rich import print


@dataclass()
class ChromeBot:
    url: str
    timeout: float

    def extract_account_names(self, driver: webdriver.Chrome) -> list[str]:
        "Extract account information from top page banner."
        driver.get(self.url)
        accounts = driver.find_elements(
            By.CSS_SELECTOR, ".postListBig .accountName"
        )
        return [account.text for account in accounts]

    def extract_account_page_urls(self, driver: webdriver.Chrome) -> list[str]:
        "Extract account information from top page banner."
        driver.get(self.url)
        accounts = driver.find_elements(By.CSS_SELECTOR, ".postListBig a")
        return [account.get_attribute("href") for account in accounts]

    def extract_photo_url(
        self, driver: webdriver.Chrome, page_url: str
    ) -> list[str]:
        "Return URLs of the photo."
        driver.get(page_url)
        photos = driver.find_elements(By.CSS_SELECTOR, "figure img")
        return [photo.get_attribute("src") for photo in photos]

    def save_photo(self, photos: list[bytes]) -> None:
        for i, photo in enumerate(photos):
            with open(f"{i:02}_photo.jpg", "wb") as f:
                f.write(photo)


if __name__ == "__main__":
    URL: str = "https://instagrammernews.com/"
    instagram = ChromeBot(URL, 5.0)
    options = webdriver.ChromeOptions()
    options.add_argument("headless=new")

    with webdriver.Chrome(options) as driver:
        driver.implicitly_wait(instagram.timeout)
        names = instagram.extract_account_names(driver)
        urls = instagram.extract_account_page_urls(driver)
        account_data = dict(zip(names, urls))
        print(account_data)
