from cloudscraper import create_scraper
from requests import Session
client = create_scraper(
            browser={"browser": "chrome", "platform": "linux", "desktop": True},
        )

r_client = Session()