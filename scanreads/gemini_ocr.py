from google import genai
from google.genai import types

from PIL import Image
from scanreads import img_to_bytes


class BookData:
    def __init__(self, author: str, publisher: str, title: str):
        self.author = author
        self.publisher = publisher
        self.title = title


class GeminiOCR:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def __call__(self, image: Image.Image) -> BookData:
        img_bytes = img_to_bytes(image)

        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                types.Part.from_bytes(
                    data=img_bytes,
                    mime_type='image/jpeg',
                ),
                'Please, write author, publisher and title of this book. Write them in one line, separated by #. If you don\'t know, write "Unknown". For example: AUTHOR#PUBLISHER#TITLE'
            ])

        text = response.text
        splits = text.split("#")

        splits = [s.strip() for s in splits]

        # Convert unknown to None
        splits = [None if s.lower() == "unknown" else s for s in splits]

        splits += [None] * 3
        splits = splits[:3]

        author, publisher, title = splits

        return BookData(
            author=author,
            publisher=publisher,
            title=title
        )
