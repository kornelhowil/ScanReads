from PIL import Image


class Reader():
    """
    A class for reading and processing image of a book
    """

    def __init__(self, gemini_api_key: str):
        """
        Initialize the Reader class with the given API keys.
        """
        self.gemini_api_key = gemini_api_key

    def __call__(self, image: Image.Image) -> dict:
        dummy_response = {
            "title": "1984",
            "author": "George Orwell",
            "publisher": "Secker & Warburg",
            "about_book": "A dystopian social science fiction novel and cautionary tale, warning of the dangers of totalitarianism and extreme political ideology.",
            "about_author": "George Orwell was an English novelist, essayist, journalist, and critic. He is best known for his novels 'Animal Farm' and '1984'.",
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
        return dummy_response
