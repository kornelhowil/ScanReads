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
                },
                {
                    "title": "The Giver",
                    "author": "Lois Lowry",
                    "publisher": "Houghton Mifflin Harcourt",
                    "image": "https://covers.openlibrary.org/b/id/14845126-M.jpg",
                },
                {
                    "title": "The Road",
                    "author": "Cormac McCarthy",
                    "publisher": "Alfred A. Knopf",
                    "image": "https://covers.openlibrary.org/b/id/14845126-M.jpg",
                }
            ]
        }
        return dummy_response
