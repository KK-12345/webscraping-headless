from datetime import datetime
import asyncio
from utils.constants import AmazonQuerySelectors


async def get_reviews_for_elements(review_elements, selectors):
    """
    # Common method to get the reviews for elements
    """
    reviews = await asyncio.gather(
        *[process_review(review_element, selectors) for review_element in review_elements])
    return reviews


async def process_review(review_element, selectors):
    """
    # Processes one element and gets reviews
    """

    review_title = await extract_review_title(review_element,
                                                       selectors.REVIEW_TITLE.value)
    review_body = await extract_review_body(review_element,
                                                     selectors.REVIEW_BODY.value)
    review_date = await extract_review_date(review_element,
                                                     selectors.REVIEW_DATE.value)
    rating = await extract_rating(review_element, selectors.REVIEW_RATING.value)

    return {
        "review_title": review_title,
        "review_body": review_body,
        "review_date": review_date,
        "rating": rating
    }


async def extract_review_title(review_element, query_selector):
    """
    # Extracts title of the review
    # @param review_element: Review Element
    # @type review_element: JS element
    # @param query_selector: selector for element
    # @type: str
    """
    try:
        title = await review_element.evaluate(
            f"(element) => element.querySelector('{query_selector}').innerText")
        title = title.replace("\n", "")
        title = title.strip()
    except:
        title = "not available"
    return title

async def extract_review_body(review_element, query_selector):
    """
        # Extracts Body of the review
        # @param review_element: Review Element
        # @type review_element: JS element
        # @param query_selector: selector for element
        # @type: str
        """
    try:
        body = await review_element.evaluate(
            f"(element) => element.querySelector('{query_selector}').innerText")
        body = body.replace("\n", "")
        body = body.strip()
    except:
        body = "not available"
    return body

async def parse_date_for_amazon(date):
    date = date.split()[-3:]
    date = " ".join(date)
    date = datetime.strptime(date, '%d %B %Y')
    date = date.strftime('%d %B %Y')
    return date

async def extract_review_date(review_element, query_selector):
    """
        # Extracts title of the review
        # @param review_element: Review Element
        # @type review_element: JS element
        # @param query_selector: selector for element
        # @type: str
        # @param site: Site Amz/Flipkart
        # @type: str
        """
    try:
        date = await review_element.evaluate(
            f"(element) => element.querySelector('{query_selector}').innerText")
        if query_selector is AmazonQuerySelectors.REVIEW_DATE:
            date = await parse_date_for_amazon(date)
    except:
        date = "not available"
    return date


async def extract_rating(review_element, query_selector):
    """
        # Extracts rating of the review
        # @param review_element: Review Element
        # @type review_element: JS element
        # @param query_selector: selector for element
        # @type: str
        """
    try:
        ratings = await review_element.evaluate(
            f"(element) => element.querySelector('{query_selector}').innerText")
    except:
        ratings = "not available"
    return ratings.split()[0]
