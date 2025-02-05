from scrapping.async_amazon_utils import AmazonScrapingUtils
from scrapping.async_flipkart_utils import FlipkartScrapingUtils
                                                  # start_scraping, navigate_to_reviews, get_product_details)
from scrapping.abstract_base import AbstractScraper
from utils.config_parser import ConfigParser
from utils.logging import logger


class AmazonScraper(AbstractScraper):
    """Scraper crated for Amazon"""
    def __init__(self):
        self.amazon_utils = None
        self.config = ConfigParser().to_json()

    async def create(self):
        """Creates a scraper and initialises utils"""
        logger.debug(f"Creating a scraper for Amazon")
        self.amazon_utils = await AmazonScrapingUtils.create(self.config)
        logger.debug(f"Created a scraper for the Amazon")
        return self


    async def navigate_to_reviews(self, url: str):
        # url = await self.amazon_utils.navigate_to_reviews(url)
        pass

    async def scrape(self, url):
        """
        # Scrapes the product reviews from Amazon
        # @param url: url for the product
        # @type url: str
        """
        logger.info("Scraping the reviews for amazon")
        reviews = await self._scrape_reviews(url)
        logger.info("Scraped the reviews for te amazon")
        return reviews

    async def get_product_details(self, url: str):
        # product_details = await self.amazon_utils.get_product_details(url)
        # return product_details
        pass
    async def _scrape_reviews(self, url: str):
        reviews = []
        reviews = await self.amazon_utils.start_scraping(url=url)
        return reviews


class FlipkartScraper(AbstractScraper):
    """Scraper created for Flipkart"""
    def __init__(self):
        self.flipkart_utils = None
        self.config = ConfigParser().to_json()

    async def create(self):
        """
        Creates self object for Flipkart Scraper
        """
        logger.debug("Crating a Flipkart Scraper instance")
        self.flipkart_utils = await FlipkartScrapingUtils.create(self.config)
        logger.debug("Created a Flipkart Scraper instance")
        return self

    async def navigate_to_reviews(self, url: str):
        """Method to navigate to products page"""
        pass
        # url = await self.flipkart_utils.navigate_to_reviews(url)

    async def scrape(self, url):
        """
        Scrapes reviews from flipkart
        @param url: url for the product page
        @type url: str
        @returns reviews: list of reviews scraped
        """
        logger.info(f"Scraping reviews for the flipkart url: {url}")
        reviews = await self._scrape_reviews(url)
        logger.info(f"Scraped the reviews for the Flipkart url: {url}")
        return reviews

    async def get_product_details(self, url: str):
        "Method to scrape product details"
        # product_details = await self.flipkart_utils.get_product_details(url)
        pass
        # return product_details

    async def _scrape_reviews(self, url: str):
        """Private method to scrape flipkart page """
        reviews = []
        reviews  = await self.flipkart_utils.start_scraping(url=url)
        return reviews
