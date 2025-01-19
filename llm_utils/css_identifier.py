import openai

def get_dynamic_css_selector(html_content: str, api_key: str) -> dict:
    """
    Use OpenAI LLM to identify dynamic CSS selectors for reviews.
    """
    openai.api_key = api_key

    prompt = f"""
    Analyze the following HTML content and provide the CSS selectors for:
    - Review Title
    - Review Body
    - Rating
    - Reviewer Name
    
    HTML:
    {html_content[:2000]}  # Truncate if too large
    
    Respond in JSON format:
    {{
        "title_selector": "...",
        "body_selector": "...",
        "rating_selector": "...",
        "reviewer_selector": "..."
    }}
    """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )

    return response['choices'][0]['text']
