import json

from google import genai
from google.genai import types
from google_books_api_wrapper.api import GoogleBooksAPI


class BookParams:
    def __init__(self, page_count: int, description: str, author_description: str, cover_url: str):
        self.page_count = page_count
        self.description = description
        self.author_description = author_description
        self.cover_url = cover_url


class BookParamGetter:
    def __init__(self, api_key: str):
        self.api = GoogleBooksAPI()
        self.client = genai.Client(api_key=api_key)
        self.search = types.Tool(
            google_search=types.GoogleSearch()
        )

    def get_book_params(self, book_title: str, author: str, full=True) -> BookParams:
        book = self.api.search_book(book_title, author=author).get_best_match()
        
        if book is not None: 
            img_url = book.large_thumbnail
            description = book.description
            author_description = None
            page_count = book.page_count
        else:
            img_url = None
            description = None
            author_description = None
            page_count = None
            full = False

        if full:
            if description is None or len(description) < 10:
                description = self.client.models.generate_content(
                    model='gemini-2.5-flash-preview-04-17',
                    contents=f"Write a short description of the book '{book_title}' by {author}. I have no idea about it. Do your best to sum it up. Make sure to sound like you are certain. Do not use words like 'probably' or 'likely'. Keep it under 50 words.",
                    config=types.GenerateContentConfig(
                        tools=[self.search],
                        response_modalities=["TEXT"],
                        )
                ).text

            author_description = self.client.models.generate_content(
                model='gemini-2.5-flash-preview-04-17',
                contents=f"Write a short description of the author {author}. I have no idea about him/her, but I know that he wrote {book_title}. Write speculations available to you due to your search (but note that you are not sure in case of ambiguity). Do not write only that he wrote the book, we know that. Do your best to sum it up. If you don't know say 'He/She is a person (probably).'. In that case do not add anything else. Keep it under 100 words.",
                config=types.GenerateContentConfig(
                        tools=[self.search],
                        response_modalities=["TEXT"],
                )
            ).text

        return BookParams(
            page_count=page_count,
            description=description,
            author_description=author_description,
            cover_url=img_url
        )
