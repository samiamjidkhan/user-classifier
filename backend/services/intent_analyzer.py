# services/intent_analyzer.py
from typing import Tuple, List
import groq

class IntentAnalyzer:
    def __init__(self, api_key: str):
        self.client = groq.Groq(api_key=api_key)

    def generate_intent_question(self, content: str) -> Tuple[str, List[str]]:
        """
        Analyze website content and generate a question with multiple-choice options
        to classify visitor intent.
        
        Args:
            content (str): The scraped website content
            
        Returns:
            Tuple[str, List[str]]: A tuple containing (question, list of options)
        """
        prompt = f"""Analyze the following website content and create a single multiple-choice question that would help classify a visitor's primary intent or interest. The question should be focused on understanding what category or type of content the visitor is most interested in.

Content: {content}

Generate:
1. A clear, concise question about the visitor's primary interest
2. Exactly 4 multiple-choice options (A through D) that cover the main categories or themes found in the content
3. Options should be mutually exclusive and collectively exhaustive
4. Each option should be brief (1-5 words)

Format your response exactly like this example:
Question: Which product category are you interested in?
A) Smartphones
B) Laptops
C) Smart Home
D) Wearables

Your response:"""

        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing website content and creating targeted questions to understand visitor intent. Focus on the main categories or themes present in the content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200,
        )

        # Parse the response
        response_text = response.choices[0].message.content.strip()
        lines = [line.strip() for line in response_text.split('\n') if line.strip()]
        
        # Extract question and options
        question = lines[0].replace('Question: ', '')
        options = [opt.strip().replace(f'{letter}) ', '') 
                  for letter, opt in zip(['A', 'B', 'C', 'D'], lines[1:])]

        return question, options