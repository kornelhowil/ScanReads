from PIL import Image
from scanreads import GeminiOCR, Reader, BookParamGetter

class ScanreadsReader(Reader):
    """
    A class for reading and processing image of a book
    """

    def __init__(self, gemini_api_key: str):
        """
        Initialize the Reader class with the given API keys.
        """
        self.gemini_api_key = gemini_api_key
        
        self.gemini_ocr = GeminiOCR(
            api_key=gemini_api_key
        )
        
        self.book_param_getter = BookParamGetter(
            api_key=gemini_api_key
        )

    def __call__(self, image: Image.Image) -> dict:
        book_data = self.gemini_ocr(image)
        book_params = self.book_param_getter.get_book_params(
            book_data.title,
            book_data.author
        )
        
        response = {
            "title": book_data.title,
            "author": book_data.author,
            "publisher": book_data.publisher,
            "about_book": book_params.description,
            "about_author": book_params.author_description,
            "recommendations": [
                {
                    "title": "Brave New World",
                    "author": "Aldous Huxley",
                    "publisher": "Chatto & Windus",
                    "image": "https://covers.openlibrary.org/b/id/14845126-M.jpg",
                },
                {
                    "title": "Fahrenheit 451",
                    "author": "Ray Bradbury",
                    "publisher": "Ballantine Books",
                    "image": "https://covers.openlibrary.org/b/id/14845126-M.jpg",
                },
                {
                    "title": "The Handmaid's Tale",
                    "author": "Margaret Atwood",
                    "publisher": "McClelland & Stewart",
                    "image": "https://covers.openlibrary.org/b/id/14845126-M.jpg",
                }
            ]
        }
        return response