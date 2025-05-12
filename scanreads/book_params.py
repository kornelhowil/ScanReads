import json 

from google import genai
from google.genai import types

from google_books_api_wrapper.api import GoogleBooksAPI


class BookParams:
    def __init__(self, page_count: int, description: str, author_description: str):
        self.page_count = page_count
        self.description = description
        self.author_description = author_description

class BookParamGetter:
    def __init__(self, api_key: str):
        self.api = GoogleBooksAPI()
        self.client = genai.Client(api_key=api_key)
        self.search = types.Tool(
            google_search_retrieval=types.GoogleSearchRetrieval()
        )

    def get_book_params(self, book_title: str, author: str) -> BookParams:
        book = self.api.search_book(book_title, author=author).get_best_match()
        
        description = book.description
        
        if description is None or len(description) < 10: 
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"Write a short description of the book '{book_title}' by {author}. I have no idea about it. Do your best to sum it up.",
                #config=types.GenerateContentConfig(
                #    tools=[self.search]
            )
            
            description = response.text
            
        author_description = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Write a short description of the author {author}. I have no idea about him/her. Do your best to sum it up.",
        ).text 
        
        return BookParams(
            page_count=book.page_count,
            description=description,
            author_description=author_description
        )