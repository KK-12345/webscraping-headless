from typing import List

from utils.exceptions import UnsupportedSiteException
from utils.logging import logger
from scrapping.scraper_factory import FactoryCreator
from utils.constants import ScrapingSites


class ScrapingManager:
    def __init__(self, url: str):
        self.url = url
        self.site = self._detect_site()

    def _detect_site(self) -> str:
        """
        # Method to detect site
        # @returns site: str
        # Raises: UnsupportedSiteException
        """
        if "amazon" in self.url.lower():
            logger.info("Site detected: amazon")
            return ScrapingSites.AMAZON.value
        elif "flipkart" in self.url.lower():
            logger.info("Site detected: flipkart")
            return ScrapingSites.FLIPKART.value
        else:
            logger.exception("Unsupported site detected")
            raise UnsupportedSiteException("Unsupported site detected")
    
    def get_factory(self):
        """
        # Get a factory
        # @returns factory of type AmazonScraperFactory or FlipkartScraperFactory
        """
        logger.debug("Creating a scraping factory")
        factory = FactoryCreator.create_factory(self.site)
        logger.debug("Created a scraping factory")
        return factory

    async def scrape_reviews(self) -> List[dict]:
        """
        # Method that returns the scraped reviews
        # @returns List[dict]
        """
        logger.debug("Scraping reviews for the product")
        factory = self.get_factory()
        scraper = await factory.create_scraper()
        logger.info("Scraping the reviews ")
        reviews = await scraper.scrape(self.url)
        logger.info("Scrapped the reviews")
        return reviews
