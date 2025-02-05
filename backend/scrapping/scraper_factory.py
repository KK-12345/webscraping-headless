from utils.constants import ScrapingSites
from utils.exceptions import UnsupportedSiteException
from scrapping.scrapers import AmazonScraper, FlipkartScraper
from scrapping.abstract_base import AbstractScrapingFactory
from utils.logging import logger

class FactoryCreator:

    @staticmethod
    def create_factory(site: str) -> AbstractScrapingFactory:
        """
        # Creates the factory for Amazon and Flipkart
        # @param site
        # Returns the AbstractScrapingFactory
        """
        logger.info("Inside the FactoryProducer")
        if site not in ScrapingSites.get_values():
            ex = UnsupportedSiteException()
            logger.exception(f"{ex.error_code}: {ex.message}")
            raise ex
        if site == ScrapingSites.AMAZON.value:
            logger.debug("Creating a scraping factory for Amazon")
            amazon_scraping_factory = AmazonScrapingFactory()
            logger.debug('Created scraping factory Amazon')
            return amazon_scraping_factory

        elif site == ScrapingSites.FLIPKART.value:
            logger.debug("Creating a scraping factory for Flipkart")
            flipkart_scraping_factory = FlipkartScrapingFactory()
            logger.debug("Creating a scraping factory for Flipkart")
            return flipkart_scraping_factory

class AmazonScrapingFactory(AbstractScrapingFactory):
    """Amazon Scraping Factory"""
    async def create_scraper(self):
        """Creates a scraper for amazon"""
        logger.info("Creating a scraper for Amazon")
        amazon_scraper =  await AmazonScraper().create()
        logger.info("Created a scraper for Amazon")
        return amazon_scraper


class FlipkartScrapingFactory(AbstractScrapingFactory):
    """"Flipkart Scraping Factory"""
    async def create_scraper(self):
        """Creates a scraper for flipkart"""
        logger.info("Creating a scraper for flipkart")
        flipkart_scraper = await FlipkartScraper().create()
        logger.info("Created a scraper for Flipkart")
        return flipkart_scraper