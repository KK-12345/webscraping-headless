from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from typing import List, Callable

from scrapping.scraping_manager import ScrapingManager
from utils.rate_limiter import LeakyBucket
import asyncio

from utils.logging import logger
from utils.config_parser import ConfigParser

configparser = ConfigParser()

leak_rate = float(configparser.get('rate_limiter', 'leak_rate', default=1.0))
capacity = int(configparser.get('rate_limiter', 'capacity', default=10))

async def lifespan(app: FastAPI):
    # Leaky bucket as a rate limiter
    scraping_manager = None
    try:
        scraping_manager = ScrapingManager()
    except:
        logger.exception("Problem loading config")

    app.state.scraping_manager = scraping_manager
    bucket = LeakyBucket(leak_rate=leak_rate, capacity=capacity)
    app.state.bucket = bucket


    asyncio.create_task(bucket.leak())

    yield



app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def rate_limiter(request: Request, call_next: Callable):
    """This middleware checks if the request can be processed or rate-limited"""
    bucket = app.state.bucket
    response = None
    try:
        logger.info('Adding a request to bucket')
        bucket.add_request()
        logger.info('inside rate limiter')
        response = await call_next(request)

    except HTTPException as e:

        if e.status_code == 429:
            wait_time = bucket.get_wait_time()
            logger.exception(f"Too Many Requests, wait for :{wait_time}")
            response = ReviewResponse(
                error= f"Too Many Requests, wait for :{wait_time}",
                status_code= e.status_code,
                reviews = [],
                status="failed"
            )
    return response

class ReviewResponse(BaseModel):
    reviews: List[dict]
    status: str
    status_code: int
    error: str

def find_scraping_strategy(url: str):
    if "amazon" in url:
        return "amazon"
    elif "flipkart" in url:
        return "flipkart"
    else:
        raise ValueError("Unsupported site")


@app.get("/api/scrape_reviews", response_model=ReviewResponse)
async def scrape_reviews(url: str = Query(..., title="URL of the product")):

    scraping_manager = app.state.scraping_manager
    reviews = []

    if not url:
        logger.exception("URL parameter is missing")
        return ReviewResponse(reviews=reviews, status_code=400,
                              error="URL parameter is missing", status="failed")

    try:
        await scraping_manager.start_manager(url)
        reviews = await scraping_manager.scrape_reviews()
        return ReviewResponse(reviews=reviews, status_code=200, status='success', error='')
    except Exception as ex:
        logger.exception(f"Failed to scrape the reviews due to internal error: {str(ex)}")
        return ReviewResponse(reviews=reviews, status_code=500, error="Failed to scrape the reviews due to internal error", status="failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
