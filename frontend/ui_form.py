import os
import streamlit as st
import requests
import math
from datetime import datetime

if 'page' not in st.session_state:
    st.session_state.page = 0
backend_url = os.getenv('BACKEND_URL', 'http://localhost:8000')
reviews_per_page = int(os.getenv('REVIEWS_PER_PAGE', 5))


def fetch_reviews_from_api(url):
    try:
        response = requests.get(f"{backend_url}/api/scrape_reviews?url={url}")
        response.raise_for_status()
        reviews = response.json()
        return reviews
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        # print(reviews)
    except Exception as err:
        st.error(f"Error occurred: {err}")
    return {"reviews": []}

st.title("Product Review Scraper")


def generate_page_data():
    print('Computing start and end')
    start_idx = st.session_state.page * reviews_per_page
    reviews = st.session_state.get('reviews')
    total_reviews = len(reviews)
    end_idx = min((st.session_state.page + 1) * reviews_per_page, total_reviews)
    reviews_to_display = reviews[start_idx:end_idx]
    return reviews_to_display


def display_page_data():
    displaying = generate_page_data()
    for review in displaying:
        # date = review['review_date'] if review['review_date'] else str(datetime.now().date())
        date = str(datetime.now().date())
        review_date = datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')

        if 'review_container' not in st.session_state:
            st.session_state['review_container'] = []
        st.session_state['review_container'] = []
        with st.container():
            col1, col2 = st.columns([3, 5])
            with col1:
                st.markdown(f"**Title**: {review['review_title']}")
                st.write(f"**Rating**: {review['rating']} stars")
            with col2:
                st.write(f"**Review**: {review['review_body']}")
                st.write(f"**Date**: {review['review_date']}")
            st.write("---------****------")

reviews = []
if not st.session_state.get('reviews', []):
    product_url = st.text_input("Enter Amazon or Flipkart product URL:")
    if st.button("Scrape Reviews"):
        if product_url:
            result = fetch_reviews_from_api(product_url)
            reviews = result.get("reviews", [])
            st.session_state.update({'reviews': reviews})
            total_reviews = len(reviews)                             
            total_pages = math.ceil(total_reviews / reviews_per_page)
            st.session_state.update({'total_pages': total_pages})    
        else:
            st.warning("Please enter a valid product URL.")

def manage_buttons(total_pages):
    col1, col2, col3 = st.columns([2, 5, 2])
    with col2:
        if st.session_state.page < total_pages-1:
            if st.button("Next", key="next"):
                print("Next button clicked")
                st.session_state.page += 1
        if st.session_state.page > 0:
            if st.button("Previous", key="prev"):
                print("Prev button clicked")
                st.session_state.page -= 1
        st.write(f"Page {st.session_state.page + 1} of {total_pages}")
        display_page_data() 

if st.session_state.get('reviews', []):
    # st.session_state.update({'reviews': reviews})
    print('inside review')
    # display_page_data()
    total_pages = int(st.session_state.get('total_pages'))
    manage_buttons(total_pages)
else:
    st.write("No reviews found.")
