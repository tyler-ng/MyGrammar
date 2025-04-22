import os
import openai
from django.conf import settings

class OpenAIService:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY', '')
        openai.api_key = self.api_key

    def refine_text(self, text):
        if not self.api_key:
            raise ValueError("OpenAI API key is not set")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that improves grammar and writing style."},
                    {"role": "user", "content": f"Refine the following text to improve grammar and clarity, while maintaining the original meaning: \n\n{text}"}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            # Extract refined text from the API response
            refined_text = response.choices[0].message['content'].strip()
            return refined_text
        
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: \{str(e)}")