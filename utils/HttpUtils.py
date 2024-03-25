from cloudscraper import create_scraper
from requests import Session
import os
client = create_scraper(
            browser={"browser": "chrome", "platform": "linux", "desktop": True},
        )

r_client = Session()

class EnvTest:
    postfix = os.environ.get('postfix')