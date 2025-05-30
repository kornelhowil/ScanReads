from PIL import Image
from scanreads import GeminiOCR, Reader, BookParamGetter, RecommendationGenerator


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

        self.recommendation_generator = RecommendationGenerator(
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
            "page_count": book_params.page_count,
        }

        recommendations = self.recommendation_generator.generate_recommendations(
            book_data.title,
            book_data.author
        )

        response["recommendations"] = []

        for recommendation in recommendations:
            print("R2", recommendation.title)
            print("R3", recommendation.author)

            params = self.book_param_getter.get_book_params(
                recommendation.title,
                recommendation.author,
                full=False
            )

            print("R4", params.cover_url, type(params.cover_url))

            response["recommendations"].append({
                "title": recommendation.title,
                "author": recommendation.author,
                "publisher": "Unknown",
                "image": params.cover_url,
            })
        
        # More niche books (or made up ones) won't have cover_url
        # as such, we sort them to the end of the list and limit up to 3
        # recommendations.
        
        response["recommendations"] = sorted(
            response["recommendations"],
            key=lambda x: x["image"] is not None,
            reverse=True
        )
        
        if len(response["recommendations"]) > 3:
            # Limit to 3 recommendations
            response["recommendations"] = response["recommendations"][:3]
        elif len(response["recommendations"]) < 3:
            # Fill with None if less than 3 recommendations
            response["recommendations"] += [{"title": None, "author": None, "publisher": "Unknown", "image": None}] * (3 - len(response["recommendations"]))      

        return response
