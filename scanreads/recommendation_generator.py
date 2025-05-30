from google import genai
from google.genai import types

class Recommendation:
    def __init__(self, author: str, title: str):
        self.author = author
        self.title = title
    
class RecommendationGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.search = types.Tool(
            google_search=types.GoogleSearch()
        )
        
    def generate_recommendations(self, book_title: str, author: str) -> list[Recommendation]:
        response = self.client.models.generate_content(
            model='gemini-2.5-flash-preview-04-17',
            contents=f"You are roleplaying as Mr. Technicality Man that follows instructions as closely as possible, why remaining as shy and laconic as possible. Please, write 5 book recommendations based on the book '{book_title}' by {author}. Write them in one line, separated by #. Start your answer with | sign for parsing. DO NOT WRITE ANYTHING ELSE. I REPEAT: FOLLOW EXAMPLE AS CLOSELY AS YOU CAN. YOU WILL BREAK CHARACTER OTHERWISE. Example: |AUTHOR#TITLE#AUTHOR#TITLE#AUTHOR#TITLE",
            config=types.GenerateContentConfig(
                        tools=[self.search],
                        response_modalities=["TEXT"],
            )
        )
        
        text = response.text
        
        try:
            text = text.split("|")[-1]
        except IndexError:
            return [] 
        
        recommendations = text.split("#")
        
        recommendations = [r.strip() for r in recommendations]
        
        pairs = zip(recommendations[::2], recommendations[1::2])
        recommendations = [Recommendation(author=author, title=title) for author, title in pairs]
        
        return recommendations