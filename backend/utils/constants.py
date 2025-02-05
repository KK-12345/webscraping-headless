from enum import Enum

class GenericConstants(Enum):
    DEFAULT_CONFIG_LOCATION = "config/config.json"
    PROJECT_ROOT_LOCATION = ""
    SECURE_PASSPHRASE = "my_secure_passphrase"

class ScrapingSites(Enum):
    AMAZON = 'amazon'
    FLIPKART = 'flipkart'

    @staticmethod
    def get_values():
        return {scraping_site.value for scraping_site in ScrapingSites}

class AmazonQuerySelectors(Enum):
    REVIEW_TITLE = '[data-hook="review-title"]'
    REVIEW_BODY = '[data-hook="review-body"]'
    REVIEW_DATE = '[data-hook="review-date"]'
    REVIEW_RATING = '[data-hook="review-star-rating"]'

class FlipkartQuerySelectors(Enum):
    REVIEW_TITLE = '.z9E0IG'
    REVIEW_BODY = '.ZmyHeo'
    REVIEW_DATE = '._2NsDsFhj'
    REVIEW_RATING = 'div.XQDdHH.Ga3i8K'