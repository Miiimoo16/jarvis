import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEME = (
    "Tu es JARVIS, assistant personnel élégant, concis et un peu espiègle. "
    "Tu réponds TOUJOURS et UNIQUEMENT en français, en 1 à 3 phrases courtes. "
    "N'utilise jamais une autre langue(sauf si je te le demande), ni emojis, ni listes, ni symboles."
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