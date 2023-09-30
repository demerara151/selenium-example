"""Example of scraping images using context manager with selenium manager"""
from selenium import webdriver
import uuid
import asyncio
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from rich import print
import httpx
from selectolax.parser import HTMLParser

URL: str = "https://instagrammernews.com/"
options = webdriver.ChromeOptions()
options.add_argument("headless=new")  # type:ignore


@dataclass(slots=True)
class InstagramExtractor:
    website: str

    def extract_post_urls(self, driver: webdriver.Chrome) -> list[str]:
        """
        Extracts latest post's URL from the specified website.

        Args:
            driver: A Selenium ChromeDriver object.

        Returns:
            A list of latest post's URLs.
        """
        driver.get(self.website)
        links = driver.find_elements(By.CSS_SELECTOR, ".postListBig li a")
        return [
            link.get_attribute("href") or "" for link in links  # type: ignore
        ]

    async def create_database(
        self, profile_pages: list[str]
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
        parser = InstagramParser()
        extractor = GenericExtractor()
        html_list = await extractor.fetch_all_html(profile_pages)
        try:
            async with asyncio.TaskGroup() as tg:
                database = [
                    await tg.create_task(
                        parser.extract_username_and_img_urls(html)
                    )
                    for html in html_list
                ]
        except* Exception as eg:
            for error in eg.exceptions:
                print(error)
            raise
        else:
            return database


@dataclass(slots=True)
class InstagramParser:
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


@dataclass(slots=True)
class GenericExtractor:
    async def _fetch_html(self, url: str) -> str:
        """
        Retrieves the HTML from the specified URL.

        Args:
            page_url: The URL of the HTML to retrieve.

        Returns:
            The retrieved HTML.
        """
        async with httpx.AsyncClient(timeout=1.0) as client:
            response = await client.get(url)
            html = response.text
            return html

    async def fetch_all_html(self, urls: list[str]) -> list[str]:
        """
        Fetches the HTML from the specified URLs asynchronously.

        Args:
            urls: A list of URLs to fetch the HTML from.

        Returns:
            A list of the retrieved HTML.
        """
        try:
            async with asyncio.TaskGroup() as tg:
                html = [
                    await tg.create_task(self._fetch_html(url)) for url in urls
                ]
        except* Exception as eg:
            for error in eg.exceptions:
                print(error)
            raise
        else:
            return html


@dataclass(slots=True)
class ImageDownloader:
    async def _fetch_image(self, username: str, img_url: str) -> None:
        """
        Downloads and saves an image from the specified URL.

        Args:
            username: The username.
            img_url: The URL of the image to download.

        Returns:
            The image bytes.
        """
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(img_url)
            response.raise_for_status()
            img = response.content
            filename = f"img\\{username}-{uuid.uuid4()}.jpg"
            print(f"Write an image to {filename}")
            with open(filename, "wb") as f:
                f.write(img)

    async def fetch_all_images(
        self, database: list[dict[str, list[str]]]
    ) -> None:
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
        downloader = ImageDownloader()
        async with asyncio.TaskGroup() as tg:
            [
                await tg.create_task(downloader._fetch_image(name, link))
                for record in database
                for name, links in record.items()
                for link in links
            ]


if __name__ == "__main__":
    # Extract post URLs
    instagram = InstagramExtractor(URL)
    with webdriver.Chrome(options) as driver:
        driver.implicitly_wait(5.0)
        urls = instagram.extract_post_urls(driver)
        print(urls)

    # Create database
    database = asyncio.run(instagram.create_database(urls))
    print(database)

    # Download images
    downloader = ImageDownloader()
    asyncio.run(downloader.fetch_all_images(database))
