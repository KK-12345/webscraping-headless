import asyncio
import math

import scrapping.utils as sc_utils
from playwright.async_api import async_playwright

from utils.config_parser import ConfigParser
from utils.decorators import retry_async
from utils.constants import AmazonQuerySelectors
from utils.logging import logger
from utils.exceptions import LoginCredsMissing
from utils import utils as common_utils


class AmazonScrapingUtils:

    def __init__(self, config):
        self.page = None
        self.context = None
        logger.info("Initialising Amazon scraper utils")
        self.load_config(config)

    def load_config(self, config):
        try:
            config = config['amazon']
            self.login_url = config['login_url']
            self.username = config['username']
            self.password = common_utils.decrypt_data(config['password'])
            self.max_pages_to_scrape = int(config['max_pages_to_scrape'])
            self.max_retries = int(config['max_retries'])
            self.delay = int(config['delay'])

        except (KeyError, TypeError) as ex:
            raise ex

    @classmethod
    async def create(cls, config: dict):
        """
        # Creates an instance of amazon scraping utils
        """
        logger.debug(f"Creating an instance of: {cls.__name__}")
        instance = cls(config)
        await instance.init()
        logger.debug(f"Created an instance of: {cls.__name__}")
        return instance

    async def init(self):
        logger.info("Initialising...")

        self.headers = {
            'authority': 'www.amazon.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'user-agent': 'Mozilla/5.0 (Ubuntu; Linux x86_64) AppleWebKit/537.36'
        }
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=True)

        logger.debug("Creating the context")
        self.context = await browser.new_context()
        await self.context.set_extra_http_headers(headers=self.headers)
        self.page = await self.context.new_page()

    async def amazon_login(self, email, password):
        """Amazon login method"""
        if not email and not password:
            logger.exception("Either email or password is missing for Amz login")
            raise LoginCredsMissing("Either email or password missing for Amz login")
        await self.page.goto(self.login_url)

        await self.page.wait_for_selector('input[type="email"]')

        logger.info("Moved to login page, entering email")
        await self.page.fill('input[type="email"]', email)
        await self.page.click('input[type="submit"]')

        await self.page.wait_for_selector('input[type="password"]')
        await self.page.fill('input[type="password"]', password)
        await self.page.click('input[type="submit"]')

        await self.page.wait_for_selector('a#nav-link-accountList')
        logger.info("logged in successfully to Amz")

    async def get_number_of_pages(self, url):
        """
        # Get number of review pages for a product
        # params: url: str
        """
        logger.debug(f"Getting the number of view pages of a product: {url}")
        page = await self.context.new_page()
        await self.perform_request(link=url, page=page)
        await page.wait_for_selector("[data-hook='cr-filter-info-review-rating-count']")
        pagination_selector = await page.query_selector("[data-hook='cr-filter-info-review-rating-count']")

        text = await pagination_selector.inner_text()
        num_reviews = min([int(page_num.replace(',','')) for page_num in text.strip('\n').split() if page_num.replace(',', '').isdigit()])
        pages = math.ceil(num_reviews / 10)
        logger.debug(f"Found pages {pages} for the product: {url}")

        return pages

    @retry_async(max_retries=5, delay=2)
    async def perform_request(self, link, page, page_num=1):
        logger.info(f"Performing a request for {link}, page: {page} page number: {page_num}")
        if page_num > 1:
            link = link + f'&page={page_num}'
        await page.goto(link)
        logger.info(f"Traversed to {link}")

    @staticmethod
    async def get_reviews_for_elements(review_elements):
        """
            Get reviews for all the elements
            @param: review_elements - list of elements
        """
        reviews = await sc_utils.get_reviews_for_elements(review_elements, AmazonQuerySelectors)
        return reviews

    async def extract_reviews_for_a_page(self, url, page_num):
        reviews = []

        try:
            logger.info(f"Extracting reviews for url: {url} and page number: {page_num} ")
            page = await self.context.new_page()
            await self.perform_request(url, page, page_num)
            await page.wait_for_selector("[data-hook='review']", timeout=60000)
            review_elements = await page.query_selector_all("[data-hook='review']")

            reviews = await self.get_reviews_for_elements(review_elements)
        except Exception as re:
            logger.exception(f"Caught an exception: {str(re)} , breaking the loop")
        finally:
            return reviews


    async def start_scraping(self, url: str):
            all_reviews = []
            try:
                await self.amazon_login(self.username, self.password)
                pages = await self.get_number_of_pages(url=url)
                if pages > self.max_pages_to_scrape:
                    pages = self.max_pages_to_scrape

                gathered_reviews = await asyncio.gather(
                    *(self.extract_reviews_for_a_page(url, page_num) for page_num in range(1, pages + 1))
                )
                all_reviews = [review for page_reviews in gathered_reviews for review in page_reviews]
                return all_reviews
            except Exception as ex:
                logger.exception(f"Caught an exception {str(ex)}")
                raise ex
            finally:
                logger.info(f"Finally closing the browser")
                await self.page.context.browser.close()

if __name__ == '__main__':
    loop = None
    try:

        async def create():
            config = ConfigParser().to_json()
            amazon_utils = await AmazonScrapingUtils.create(config)
            url = "https://www.amazon.in/OnePlus-28-85cm-11-35-inch-2-4K/product-reviews/B0CJ94J5CX/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
            reviews = await amazon_utils.start_scraping(url=url)
            for review in reviews:
                print(review)
        asyncio.run(create())
        loop = asyncio.get_event_loop()
    except Exception as ex:
        print(ex)
    finally:
        print("inside finally")

        if loop and not loop.is_closed():
            loop.close()
