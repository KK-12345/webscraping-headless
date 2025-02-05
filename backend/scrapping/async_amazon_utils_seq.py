import asyncio

import scrapping.utils as sc_utils
from playwright.async_api import async_playwright
from utils.decorators import retry_async
from utils.constants import AmazonQuerySelectors
from utils.logging import logger
from utils.exceptions import LoginCredsMissing


class AmazonScrapingUtils:

    def __init__(self):

        self.page = None
        self.headers = None
        self.context = None
        logger.info("Initialising Amazon scraper utils")
        self.amz_login_url = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"

    @classmethod
    async def create(cls):
        """
        # Creates an instance of amazon scraping utils
        """
        logger.debug(f"Creating an instance of: {cls.__name__}")
        instance = cls()
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
        # if self.context:
        #     self.page = await self.context.new_page()
        # else:
        logger.debug("Creating the context")
        self.context = await browser.new_context()
        await self.context.set_extra_http_headers(headers=self.headers)
        self.page = await self.context.new_page()

    async def amazon_login(self, page, email, password):
        """Amazon login method"""
        if not email and not password:
            logger.exception("Either email or password is missing for Amz login")
            raise LoginCredsMissing("Either email or password missing for Amz login")
        await self.page.goto(self.amz_login_url)

        await self.page.wait_for_selector('input[type="email"]')
        logger.info("Moved to login page, entering email")
        await self.page.fill('input[type="email"]', email)
        await self.page.click('input[type="submit"]')


        await self.page.wait_for_selector('input[type="password"]')

        await self.page.fill('input[type="password"]', password)
        await self.page.click('input[type="submit"]')

        # Wait for the home page to load (indicating successful login)
        await self.page.wait_for_selector('a#nav-link-accountList')
        # await self.context.storage_state(path="auth.json")
        logger.info("logged in successfully to Amz")

    @retry_async(max_retries=3, delay=2)
    async def perform_request(self, page, link):
        await self.page.goto(link)

    async def extract_reviews(self, page):

        reviews =[]
        while True:
            try:
                await self.page.wait_for_selector("[data-hook='review']")

                review_elements = await self.page.query_selector_all("[data-hook='review']")
                for review_element in review_elements:
                    review_title = await sc_utils.extract_review_title(review_element, AmazonQuerySelectors.REVIEW_TITLE.value)
                    review_body = await sc_utils.extract_review_body(review_element, AmazonQuerySelectors.REVIEW_BODY.value)
                    review_date = await sc_utils.extract_review_date(review_element, AmazonQuerySelectors.REVIEW_DATE.value, site='amazon')
                    rating = await sc_utils.extract_rating(review_element, AmazonQuerySelectors.REVIEW_RATING.value)
                    reviews.append(
                        {"review_title": review_title, "review_body": review_body, "review_date": review_date,
                         "rating": rating})
                # Find the next page button
                next_page_button = await page.query_selector("[class='li.a-last.a']")
                if not next_page_button:
                    return reviews

                # Click the next page button
                await page.click("[class='a-last']")
            except (RuntimeError, TimeoutError) as re:
                print("Exception caught: breaking the loop")
                print(re)
                return reviews
            except Exception as ex:
                print('caught an exception')
                print(ex)
                return reviews

    async def start_scraping(self, url: str):
        # move this to config
        await self.amazon_login(self.page, "shrikrishna.kadam4@gmail.com", "kk@9623194889")
        await self.perform_request(self.page, url)
        reviews = await self.extract_reviews(self.page)
        await self.page.context.browser.close()
        return reviews

if __name__ == '__main__':
    loop = None
    try:

        async def create():
            amazon_utils = await AmazonScrapingUtils.create()
            url = "https://www.amazon.in/OnePlus-28-85cm-11-35-inch-2-4K/dp/B0CJ94J5CX/?_encoding=UTF8&pd_rd_w=RTfhH&content-id=amzn1.sym.509965a2-791b-4055-b876-943397d37ed3%3Aamzn1.symc.fc11ad14-99c1-406b-aa77-051d0ba1aade&pf_rd_p=509965a2-791b-4055-b876-943397d37ed3&pf_rd_r=HA65NDWZH0X7E44F18QN&pd_rd_wg=cwHO7&pd_rd_r=01b5b259-097f-4c5c-b701-655e4b921d4c&ref_=pd_hp_d_atf_ci_mcx_mr_ca_hp_atf_d&th=1"
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
