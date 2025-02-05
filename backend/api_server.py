from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from typing import List, Callable
from fastapi.responses import JSONResponse
from utils.rate_limiter import LeakyBucket
import asyncio
from scrapping.scraping_manager import ScrapingManager
from utils.logging import logger
from utils.config_parser import ConfigParser

configparser = ConfigParser()

leak_rate = float(configparser.get('rate_limiter', 'leak_rate', default=1.0))
capacity = int(configparser.get('rate_limiter', 'capacity', default=10))

async def lifespan(app: FastAPI):
    # Leaky bucket as a rate limiter

    bucket = LeakyBucket(leak_rate=leak_rate, capacity=capacity)
    app.state.bucket = bucket

    asyncio.create_task(bucket.leak())

    yield

   # shutting down tasks


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
            response = JSONResponse(
                content= {"detail": "Too Many Requests", "wait_time": wait_time},
                status_code= e.status_code
            )
    return response

class ReviewResponse(BaseModel):
    reviews: List[dict]

def find_scraping_strategy(url: str):
    if "amazon" in url:
        return "amazon"
    elif "flipkart" in url:
        return "flipkart"
    else:
        raise ValueError("Unsupported site")


@app.get("/api/scrape_reviews", response_model=ReviewResponse)
async def scrape_reviews(url: str = Query(..., title="URL of the product")):
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is missing")

    try:
        manager = ScrapingManager(url)
        reviews = await manager.scrape_reviews()
        return ReviewResponse(reviews=reviews)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Failed to scrape the reviews : {str(ex)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
