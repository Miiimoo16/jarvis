import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEME = (
    "Tu es JARVIS, assistant personnel élégant, concis et un peu espiègle. "
    "Tu réponds en français, en 1 à 3 phrases courtes."
)


class Cerveau:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("BRAIN_BASE_URL"),
            api_key=os.getenv("BRAIN_API_KEY"),
        )
        self.modele = os.getenv("BRAIN_MODEL")
        self.historique = []

    def repondre(self, texte):
        self.historique.append({"role": "user", "content": texte})
        messages = [{"role": "system", "content": SYSTEME}] + self.historique[-20:]
        rep = self.client.chat.completions.create(model=self.modele, messages=messages)
        reponse = rep.choices[0].message.content
        self.historique.append({"role": "assistant", "content": reponse})
        return reponse