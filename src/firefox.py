# type: ignore
"Scrape the book cover with title using Firefox Browser."
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass(slots=True, frozen=True)
class BookScraper:
    base_url: str = "https://books.toscrape.com/"

    @property
    def _driver(self) -> webdriver.Firefox:
        "Gecko driver."
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")  # add single dash
        driver = webdriver.Firefox(options)
        driver.implicitly_wait(10)
        return driver

    def fetch_thumbnails(self) -> list[dict[str, str | None]]:
        with self._driver as driver:
            driver.get(self.base_url)
            elements = driver.find_elements(By.CSS_SELECTOR, "img.thumbnail")
            return [
                {
                    "title": element.get_attribute("alt"),
                    "link": element.get_attribute("src"),
                }
                for element in elements
            ]


if __name__ == "__main__":
    from rich import print

    fetcher = BookScraper()
    data = fetcher.fetch_thumbnails()
    print(data)
