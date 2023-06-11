# type: ignore
"""Scrape color information from https://www.colordic.org/w"""
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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
    profile: str = "Profile 1"

    def get_all_texts_from_elements(self, *, url: str, xpath: str) -> None:
        """
        Load web page and scrape all the information of every colors.
        Write them as csv data to the `colors.csv`.

        Parameter
        ---
        url: The URL of web site that contains color information.
        xpath: XPath of desired elements.

        Return
        ---
        Nothing returns. Quit the web driver and close the browser.

        """

        service = ChromeService(
            executable_path=ChromeDriverManager().install(),
        )

        options = webdriver.ChromeOptions()

        # from selenium 4.8.0, have to specify headless mode explicitly
        # see https://www.selenium.dev/blog/2023/headless-is-going-away/
        options.add_argument("headless=new")

        options.add_argument(f"profile-directory={self.profile}")

        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable(("xpath", xpath))
        )

        colors = driver.find_elements("xpath", xpath)

        csv_data: list[str] = [
            color.get_attribute("title").replace(" ", ",") for color in colors
        ]

        with Path("colors.csv").open("a") as f:
            f.write("name,read,code\n")
            f.writelines(csv_data)

        driver.quit()


if __name__ == "__main__":
    spider = WebScraper()
    spider.get_all_texts_from_elements(
        url="https://www.colordic.org/w", xpath="//table/tbody/tr/td/a"
    )
