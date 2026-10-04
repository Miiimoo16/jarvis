import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from outils import schemas, executer, est_direct

load_dotenv()

SYSTEME = (
    "Tu es JARVIS, assistant personnel élégant, concis et un peu espiègle. "
    "Tu réponds TOUJOURS et UNIQUEMENT en français, en 1 à 3 phrases courtes. "
    "N'utilise jamais une autre langue, ni emojis, ni listes, ni symboles. "
    "Pour toute demande d'ouvrir un site, appelle TOUJOURS l'outil ouvrir_site. "
    "Pour l'heure ou la date, appelle TOUJOURS l'outil heure_actuelle. "
    "Ne dis jamais avoir fait une action sans avoir appelé l'outil correspondant."
)


class Cerveau:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("BRAIN_BASE_URL"),
            api_key=os.getenv("BRAIN_API_KEY"),
        )
        self.modele = os.getenv("BRAIN_MODEL")
        self.historique = []

    def _messages(self):
        recents = self.historique[-20:]
        # une conversation valide doit commencer par un message utilisateur
        while recents and recents[0]["role"] != "user":
            recents = recents[1:]
        return [{"role": "system", "content": SYSTEME}] + recents

    def repondre(self, texte):
        self.historique.append({"role": "user", "content": texte})
        for _ in range(3):  # 3 tours d'outils maximum
            rep = self.client.chat.completions.create(
                model=self.modele, messages=self._messages(), tools=schemas()
            )
            msg = rep.choices[0].message
            if not msg.tool_calls:
                reponse = msg.content or ""
                self.historique.append({"role": "assistant", "content": reponse})
                return reponse
            self.historique.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            })
            resultats = []
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                resultat = executer(tc.function.name, args)
                print(f"[outil] {tc.function.name} {args} -> {resultat}")
                resultats.append(str(resultat))
                self.historique.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(resultat),
                })
            if all(est_direct(tc.function.name) for tc in msg.tool_calls):
                reponse = " ".join(resultats)
                self.historique.append({"role": "assistant", "content": reponse})
                return reponse
        return "Je n'y arrive pas pour le moment."