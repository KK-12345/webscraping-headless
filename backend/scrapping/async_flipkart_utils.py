import asyncio
from playwright.async_api import async_playwright
import scrapping.utils as sc_utils
from utils.config_parser import ConfigParser
from utils.constants import FlipkartQuerySelectors
from utils.decorators import retry_async
from utils.logging import logger

class FlipkartScrapingUtils:

    def __init__(self, config):
        self.page = None
        self.headers = None
        self.load_config(config)

    def load_config(self, config):
        try:
            config = config['flipkart']
            self.max_pages_to_scrape = int(config['max_pages_to_scrape'])
            self.max_retries = int(config['max_retries'])
            self.delay = int(config['delay'])
        except (KeyError, TypeError) as ex:
            raise ex

    @classmethod
    async def create(cls, config):
        logger.debug(f"Creating an instance of {cls.__name__}")
        instance = cls(config)
        await instance.init()
        logger.debug(f"Created an instance of {cls.__name__}")
        return instance

    async def init(self):
        logger.debug(f"Initialising..{self.__class__.__name__}")
        self.headers = {
            'authority': 'www.flipkart.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=True)
        self.context = await browser.new_context()
        await self.context.set_extra_http_headers(headers=self.headers)
        self.page = await self.context.new_page()
        logger.debug(f"Created the context and page")

    async def get_number_of_pages(self, url):
        """
        # Get number of review pages for a product
        # params: url: str
        """
        logger.debug(f"Getting the number of view pages of a product: {url}")
        page = await self.context.new_page()
        await self.perform_request(link=url, page=page)
        await page.wait_for_selector("._1G0WLw.mpIySA", timeout=5000)
        pagination_selector = await page.query_selector('._1G0WLw.mpIySA')
        text = await pagination_selector.inner_text()
        pages = max([int(page_num) for page_num in text.strip('\n').split() if page_num.isdigit()])
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
        reviews = await sc_utils.get_reviews_for_elements(review_elements, FlipkartQuerySelectors)
        return reviews

    async def extract_reviews_for_a_page(self, url, page_num):
        reviews = []

        try:
            logger.info(f"Extracting reviews for url: {url} and page number: {page_num} ")
            page = await self.context.new_page()
            await self.perform_request(url, page, page_num)
            await page.wait_for_selector(".EKFha-", timeout=60000)

            review_elements = await page.query_selector_all(".EKFha-")
            reviews = await self.get_reviews_for_elements(review_elements)

        except Exception as re:
            logger.exception(f"Caught an exception: {str(re)} , breaking the loop")
        finally:
            return reviews


    async def start_scraping(self, url: str):
        all_reviews = []
        try:
            pages = await self.get_number_of_pages(url=url)
            if pages > 5:
                pages = 5

            gathered_reviews = await asyncio.gather(
                *(self.extract_reviews_for_a_page(url, page_num) for page_num in range(1, pages+1))
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
    config = ConfigParser().to_json()
    async def create():
        flipkart_utils = await FlipkartScrapingUtils.create(config)
        url = "https://www.flipkart.com/motorola-edge-50-fusion-marshmallow-blue-128-gb/product-reviews/itmf88eea5799a27?pid=MOBGXTYZEZSZQE7W&lid=LSTMOBGXTYZEZSZQE7WIBXLBI&marketplace=FLIPKART"
        reviews = await flipkart_utils.start_scraping(url=url)
        for review in reviews:
            print(review)
    asyncio.run(create())

