# type: ignore
"""Example of scraping images using context manager with selenium manager"""
import asyncio
import uuid
from dataclasses import dataclass

from httpx import AsyncClient
from rich import print
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass(slots=True)
class InstagramFetcher:
    base_url: str = "https://instagrammernews.com/"

    @property
    def _client(self) -> AsyncClient:
        "httpx async client"
        return AsyncClient(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"
                    " Gecko/20100101 Firefox/119.0"
                )
            },
            timeout=10.0,
        )

    @property
    def _driver(self) -> webdriver.Chrome:
        "Chromedriver."
        options = webdriver.ChromeOptions()
        options.add_argument("headless=new")
        driver = webdriver.Chrome(options)
        driver.implicitly_wait(10)
        return driver

    def fetch_post_urls(self) -> list[str]:
        """
        Extracts latest post's URL from the specified website.

        Args:
            driver: A Selenium ChromeDriver object.

        Returns:
            A list of latest post's URLs.
        """
        with self._driver as driver:
            driver.get(self.base_url)
            links = driver.find_elements(By.CSS_SELECTOR, ".postListBig li a")
            return [link.get_attribute("href") or "" for link in links]

    async def _fetch_html(self, url: str) -> str:
        """
        Retrieves the HTML from the specified URL.

        Args:
            page_url: The URL of the HTML to retrieve.

        Returns:
            The retrieved HTML.
        """
        async with self._client as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text
            return html

    async def fetch_html(self, urls: list[str]) -> list[str]:
        """
        Fetches the HTML from the specified URLs asynchronously.

        Args:
            urls: A list of URLs to fetch the HTML from.

        Returns:
            A list of the retrieved HTML.
        """
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(self._fetch_html(url)) for url in urls]
        return [task.result() for task in tasks]

    async def _fetch_image(self, username: str, img_url: str) -> None:
        """
        Downloads and saves an image from the specified URL.

        Args:
            username: The username.
            img_url: The URL of the image to download.

        Returns:
            The image bytes.
        """
        async with self._client as client:
            response = await client.get(img_url)
            response.raise_for_status()
            img = response.content
            # FIXME: Image format can be png or something different.
            filename = f"img\\{username}-{uuid.uuid4()}.jpg"
            print(f"Write an image to {filename}")
            with open(filename, "wb") as f:
                f.write(img)

    async def fetch_images(self, database: list[dict[str, list[str]]]) -> None:
        """
        Downloads and saves all the images
        from the specified database asynchronously.

        Args:
            database: A list of dictionaries,
            where each dictionary represents a record in the database.
                The dictionary should contain the following keys:
                * `name`: The name of the record.
                * `links`: A list of URLs of the images to download.
        """
        async with asyncio.TaskGroup() as tg:
            _ = [
                tg.create_task(self._fetch_image(name, link))
                for record in database
                for name, links in record.items()
                for link in links
            ]
        return None


@dataclass(slots=True)
class InstagramExtractor:
    async def extract_username_and_img_urls(
        self, html: str
    ) -> dict[str, list[str]]:
        """
        Extracts the username and a list of image URLs from HTML.

        If URL is None or can't find it, returns empty string.

        Args:
            html: The HTML to extract the username and image URLs from.

        Returns:
            A dictionary containing the username as the key

            and a list of image URLs as the value.
        """
        tree = HTMLParser(html)
        images = tree.css("figure img")
        username = tree.css_first(".accountName > strong > a")
        return {
            username.text(): [
                image.attributes["src"] or "" for image in images
            ]
        }

    async def create_database(
        self, html_list: list[str]
    ) -> list[dict[str, list[str]]]:
        """
        Generates a database containing the username and image URLs
        extracted from the corresponding HTML.

        Args:
            html_list: A list of HTML.

        Returns:
            A list of dictionaries,
            where each dictionary contains the username and image URLs
        """

        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(self.extract_username_and_img_urls(html))
                for html in html_list
            ]
        return [task.result() for task in tasks]


if __name__ == "__main__":
    # Extract post URLs
    fetcher = InstagramFetcher()
    urls = fetcher.fetch_post_urls()
    list_html = asyncio.run(fetcher.fetch_html(urls))

    # Create database
    extractor = InstagramExtractor()
    database = asyncio.run(extractor.create_database(list_html))
    print(database)

    # Download images
    asyncio.run(fetcher.fetch_images(database))
