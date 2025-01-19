from fastapi import FastAPI, Query
from playwright.sync_api import sync_playwright
from llm_utils.css_identifier import get_dynamic_css_selector

app = FastAPI()

OPENAI_API_KEY = "your_openai_api_key"  # Replace with your OpenAI API Key

@app.get("/api/reviews")
def get_reviews(page: str = Query(..., description="URL of the page to scrape")):
    try:
        with sync_playwright() as p:
            # Initialize headless browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page_instance = context.new_page()
            page_instance.goto(page)

            # Extract HTML content of the page
            html_content = page_instance.content()

            # Use LLM to identify dynamic CSS selectors
            css_selectors = get_dynamic_css_selector(html_content, OPENAI_API_KEY)

            # Extract review elements using dynamic CSS selectors
            reviews = []
            while True:
                review_elements = page_instance.query_selector_all(css_selectors["title_selector"])
                for element in review_elements:
                    reviews.append({
                        "title": element.query_selector(css_selectors["title_selector"]).inner_text(),
                        "body": element.query_selector(css_selectors["body_selector"]).inner_text(),
                        "rating": element.query_selector(css_selectors["rating_selector"]).inner_text(),
                        "reviewer": element.query_selector(css_selectors["reviewer_selector"]).inner_text(),
                    })

                # Handle pagination
                next_button = page_instance.query_selector('a.next')  # Modify if site uses a different pagination structure
                if next_button:
                    next_button.click()
                    page_instance.wait_for_load_state()
                else:
                    break

            browser.close()
            return {"reviews_count": len(reviews), "reviews": reviews}

    except Exception as e:
        return {"error": str(e)}
