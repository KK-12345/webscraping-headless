
from playwright.sync_api import sync_playwright



def scrape_amazon_product_details(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        title = page.query_selector('#productTitle').inner_text().strip()

        try:
            price = page.query_selector('.a-price-whole').inner_text().strip()
        except:
            price = "Price not available"

        # Close the browser
        browser.close()

        # Return the scraped details
    return {
        'title': title,
        'price': price,
        #'rating': rating
    }

def scrape_amazon_reviews(url):
    reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        # page.set_extra_http_headers(headers={'User-Agent': user_agent})

        page.goto(url)


        # see_more_reviews_link = page.locator('a:has-text("See more reviews")').first
        # see_more_reviews_link.click()
        # page.wait_for_selector('a-section a-spacing-none reviews-content a-size-base')

        # page.wait_for_selector('ul.a-unordered-list a-nostyle a-vertical', timeout=400)

        print('found the review list')
        while True:

            # review_elements = page.locator('a-section a-spacing-none review-views celwidget')
            # review_elements = page.query_selector_all('ul.a-unordered-list a-nostyle a-vertical')
            for review in review_elements:
                text = review.locator('span.a-size-base.review-text').inner_text()
                rating = review.locator('i.a-icon-star').inner_text()
                reviews.append({"review_text": text, "rating": rating.strip()})


            next_button = page.locator('li.a-last a')
            if next_button.is_enabled():
                next_button.click()
                page.wait_for_timeout(2000)
            else:
                break

        browser.close()
    
    return reviews

def scrape_flipkart_reviews(url):
    
    reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

       
        page.locator('._3U-Vxu').click()
        page.wait_for_selector('._1AtVbE')

        while True:
            
            review_elements = page.locator('._1AtVbE')
            for review in review_elements:
                text = review.locator('div._2-N8zT').inner_text()
                rating = review.locator('div._3LWZlK').inner_text()
                reviews.append({"review_text": text, "rating": rating.strip()})

            
            next_button = page.locator('a._1LKTO3')
            if next_button.is_enabled():
                next_button.click()
                page.wait_for_timeout(2000)  

                break  
        browser.close()
    
    return reviews

if __name__ == '__main__':
    scrape_amazon_reviews("https://www.amazon.in/OnePlus-28-85cm-11-35-inch-2-4K/dp/B0CJ94J5CX/ref=pd_ci_mcx_mh_mcx_views_0_title?pd_rd_w=GTKY9&content-id=amzn1.sym.fa0aca50-60f7-47ca-a90e-c40e2f4b46a9%3Aamzn1.symc.ca948091-a64d-450e-86d7-c161ca33337b&pf_rd_p=fa0aca50-60f7-47ca-a90e-c40e2f4b46a9&pf_rd_r=10YY8DS937Y5SVXJMSDF&pd_rd_wg=PuSBZ&pd_rd_r=5a5a7320-88b5-4083-8039-02762f87df5c&pd_rd_i=B0CJ94J5CX&th=1")