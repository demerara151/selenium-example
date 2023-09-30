import pytest

from src.insta_bot import InstagramParser


@pytest.mark.parametrize(
    "html, expected_result",
    [
        (
            """
            <html>
            <head>
            <title>Instagram</title>
            </head>
            <body>
            <div class="accountName">
            <strong><a href="/test_user/">test_user</a></strong>
            </div>
            <figure>
            <img src="/test_user/image1.jpg">
            </figure>
            <figure>
            <img src="/test_user/image2.jpg">
            </figure>
            </body>
            </html>
            """,
            {
                "test_user": [
                    "/test_user/image1.jpg",
                    "/test_user/image2.jpg",
                ],
            },
        ),
        (
            """
            <html>
            <head>
            <title>Instagram</title>
            </head>
            <body>
            <div class="accountName">
            <strong><a href="/test_user/">test_user</a></strong>
            </div>
            <figure>
            <img src="/test_user/image1.jpg">
            </figure>
            </body>
            </html>
            """,
            {
                "test_user": ["/test_user/image1.jpg"],
            },
        ),
        (
            """
            <html>
            <head>
            <title>Instagram</title>
            </head>
            <body>
            <div class="accountName">
            <strong><a href="/test_user/">test_user</a></strong>
            </div>
            </body>
            </html>
            """,
            {
                "test_user": [],
            },
        ),
    ],
)
async def test_extract_username_and_img_urls(
    html: str, expected_result: list[dict[str, str | list[str]]]
):
    parser = InstagramParser()
    actual_result = await parser.extract_username_and_img_urls(html)
    assert actual_result == expected_result
