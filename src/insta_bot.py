"""Example of scraping images using context manager with selenium manager"""
from selenium import webdriver
import uuid
import asyncio
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from rich import print
import httpx
from selectolax.parser import HTMLParser


@dataclass()
class ChromeBot:
    url: str

    def extract_account_info(self, driver: webdriver.Chrome) -> list[str]:
        "Extract account page URL from top page banner."
        driver.get(self.url)
        links = driver.find_elements(By.CSS_SELECTOR, ".postListBig li a")
        return [link.get_attribute("href") for link in links]  # type: ignore


@dataclass()
class Extractor:
    async def get_html(self, page_url: str) -> str:
        """
        Retrieve HTML from their profile page.

        ### Parameter:
        page_url: URL of the profile page.
        """
        async with httpx.AsyncClient(timeout=1.0) as client:
            response = await client.get(page_url)
            html = response.text
            return html

    async def extract_img_url(
        self, html: str
    ) -> dict[str, str | list[str | None]]:
        "Extract user name and list of image URLs from HTML"
        tree = HTMLParser(html)
        images = tree.css("figure img")
        username = tree.css_first(".accountName > strong > a")
        return {
            "name": username.text(),
            "links": [image.attributes["src"] for image in images],
        }

    async def fetch_img(self, img_url: str | None) -> bytes | None:
        """
        Fetch image data from extracted image URL.

        ### Parameter:
        img_url: URL of the image.
        """
        if img_url:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(img_url)
                img = response.content
                await asyncio.sleep(0.5)
                return img
        else:
            return None

    async def save_img(self, name: str, img: bytes | None) -> None:
        """
        Save image as account name with serial number.

        ### Parameter:
        name: User name.
        img: Image data must be byte object.
        """
        if img:
            print(f"Write image to {name}")
            with open(name, "wb") as f:
                f.write(img)
        else:
            print(
                """This user doesn't have any images. This gonna never happen.
                Please check your code."""
            )

    async def main(self, profile_pages: list[str]):
        """
        1. Access to each profile pages asynchronously.
        2. Create the database that contains
            user name and URL list of the images.
        3. Download those images and save it
            with `{username}_{uuid}.jpg` format.

        Gather these tasks and run asynchronously.
        """
        # Asynchronously fetch the HTML for each profile page
        async with asyncio.TaskGroup() as tg:
            html_documents = [
                await tg.create_task(self.get_html(page_url))
                for page_url in profile_pages
            ]

        # Extract the user name and image URLs from the HTML
        async with asyncio.TaskGroup() as tg:
            database = [
                await tg.create_task(self.extract_img_url(html))
                for html in html_documents
            ]

        # Asynchronously download and save the images
        async with asyncio.TaskGroup() as tg:
            [
                await tg.create_task(
                    self.save_img(
                        f"img\\{record['name']}_{uuid.uuid4()}.jpg",
                        await self.fetch_img(img_url),
                    )
                )
                for record in database
                for img_url in record["links"]
            ]


if __name__ == "__main__":
    URL: str = "https://instagrammernews.com/"
    instagram = ChromeBot(URL)
    options = webdriver.ChromeOptions()
    options.add_argument("headless=new")  # type:ignore

    with webdriver.Chrome(options) as driver:
        driver.implicitly_wait(5.0)
        pages = instagram.extract_account_info(driver)
        print(pages)

    print("Start to extract images.")
    extractor = Extractor()
    asyncio.run(extractor.main(pages))
