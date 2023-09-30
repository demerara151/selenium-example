# type: ignore
"""Scrape color information from https://www.colordic.org/w"""
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


@dataclass(slots=True, frozen=True)
class WebScraper:
    """
    Base class of web scraping

    Parameter
    ---
    timeout: How many times driver will be wait for the element
     to be appeared as page loads.

    profile: Profile directory name that should be located
     in the `~/AppData/Local/Google/Chrome/User Data`.
    """

    timeout: float = 10.0
    profile: str | None

    def get_all_texts_from_elements(self, *, url: str, selector: str) -> None:
        """
        Load web page and scrape all the information of every colors.
        Write them as csv data to the `colors.csv`.

        Parameter
        ---
        url: The URL of web site that contains color information.
        selector: XPath selector of desired elements.

        Return
        ---
        Nothing returns. Quit the webdriver and close the browser.

        """

        options = webdriver.ChromeOptions()
        options.browser_version = "Stable"

        # from selenium 4.8.0, have to specify headless mode explicitly
        # see https://www.selenium.dev/blog/2023/headless-is-going-away/
        options.add_argument("headless=new")

        if self.profile:
            options.add_argument(f"profile-directory={self.profile}")

        driver = webdriver.Chrome(options=options)

        driver.get(url)

        WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, selector))
        )

        colors = driver.find_elements(By.XPATH, selector)

        csv_data: list[str] = [
            color.get_attribute("title").replace(" ", ",") for color in colors
        ]

        with Path("colors.csv").open("a") as f:
            f.write("name,read,code\n")
            f.writelines(csv_data)

        screenshot = driver.get_screenshot_as_png()

        with Path("ScreenShot.png").open("wb") as f:
            f.write(screenshot)

        driver.quit()


if __name__ == "__main__":
    spider = WebScraper()
    spider.get_all_texts_from_elements(
        url="https://www.colordic.org/w", selector="//table/tbody/tr/td/a"
    )
