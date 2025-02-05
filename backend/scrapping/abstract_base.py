from abc import ABC, abstractmethod


class AbstractScraper(ABC):
    """Abstract scraper base class for Scrapper"""

    @abstractmethod
    async def scrape(self, url: str):
        """Abstract method for scraping"""
        pass

    @abstractmethod
    async def navigate_to_reviews(self, url: str) -> str:
        pass

    @abstractmethod
    async def get_product_details(self, url):
        pass

class AbstractScrapingFactory(ABC):
    """Abstract scraping factory which will create scraping factory"""
    @abstractmethod
    def create_scraper(self):
        pass
