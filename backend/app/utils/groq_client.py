from groq import Groq
from app.core.config import settings

class GroqClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str, model: str = "llama-3.3-70b-versatile", system: str = "", temperature: float = 0.7) -> str:
        """
        Generate a response from the Groq LLM.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=500,
        )
        return completion.choices[0].message.content.strip()