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


@dataclass()
class ChromeBot:
    url: str

    def extract_post_urls(self, driver: webdriver.Chrome) -> list[str]:
        "Extract all post page URLs from top page banner."
        driver.get(self.url)
        links = driver.find_elements(By.CSS_SELECTOR, ".postListBig li a")
        return [link.get_attribute("href") for link in links]  # type: ignore


@dataclass()
class Extractor:
    async def fetch_html(self, url: str) -> str:
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

    # TODO: class Downloader
    async def fetch_img(self, img_url: str) -> bytes:
        """
        Fetch image data from extracted image URL.

        ### Parameter:
        img_url: URL of the image.
        """
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(img_url)
            img = response.content
            await asyncio.sleep(0.1)
            return img

    async def main(self, profile_pages: list[str]) -> None:
        """
        Download all images and save it.
        """
        # Asynchronously fetch the HTML for each profile page
        html_documents = await self.fetch_all_html(profile_pages)

        # Extract the user name and image URLs from the HTML
        database = await self.create_database(html_documents)

        # TODO: class Downloader
        dw = DataWriter()
        # Asynchronously download and save the images
        async with asyncio.TaskGroup() as tg:
            [
                await tg.create_task(
                    dw.write_img(name, await self.fetch_img(link))
                )
                for record in database
                for name, links in record.items()
                for link in links
            ]

    async def create_database(
        self, html_documents: list[str]
    ) -> list[dict[str, str | list[str]]]:
        """
        Create the database contains the user name and image URLs
        by extracting them from the each HTML documents.
        """
        parser = Parser()
        try:
            async with asyncio.TaskGroup() as tg:
                database = [
                    await tg.create_task(
                        parser.extract_username_and_img_urls(html)
                    )
                    for html in html_documents
                ]
        except* Exception as eg:
            for error in eg.exceptions:
                print(error)
            raise
        else:
            return database

    # TODO: class Downloader
    async def fetch_all_html(self, profile_pages: list[str]) -> list[str]:
        # Asynchronously fetch the HTML for each profile page
        try:
            async with asyncio.TaskGroup() as tg:
                html_documents = [
                    await tg.create_task(self.fetch_html(page_url))
                    for page_url in profile_pages
                ]
        except* Exception as eg:
            for error in eg.exceptions:
                print(error)
            raise
        else:
            return html_documents


@dataclass()
class Downloader:
    pass


@dataclass()
class DataWriter:
    async def write_img(self, username: str, img: bytes) -> None:
        """
        Save an image with the username and UUID
        as the filename to the system.
        """
        filename = f"{username}-{uuid.uuid4()}.jpg"
        print(f"Write an image to {filename}")
        with open(filename, "wb") as f:
            f.write(img)


@dataclass()
class Parser:
    async def extract_username_and_img_urls(
        self, html: str
    ) -> dict[str, str | list[str]]:
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


if __name__ == "__main__":
    instagram = ChromeBot(URL)

    with webdriver.Chrome(options) as driver:
        driver.implicitly_wait(5.0)
        urls = instagram.extract_post_urls(driver)
        print(urls)

    print("Start to extract images.")
    extractor = Extractor()
    asyncio.run(extractor.main(urls))
