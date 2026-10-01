import re
from cerveau import Cerveau
from voix import parler
from oreilles import ecouter
import reveil

MOTS_QUITTER = ("exit", "quitter", "quitte")
MOTS_VEILLE = ("au revoir", "à plus tard")


def contient(texte, mots):
    propre = " " + re.sub(r"[^\w\s]", " ", texte.lower()) + " "
    propre = re.sub(r"\s+", " ", propre)
    return any(f" {mot} " in propre for mot in mots)


def conversation(cerveau):
    """Renvoie 'quitter' ou 'veille'."""
    silences = 0
    while True:
        texte = ecouter()
        if not texte:
            silences += 1
            if silences >= 2:
                return "veille"
            continue
        silences = 0
        print("Toi :", texte)
        if contient(texte, MOTS_QUITTER):
            parler("À bientôt.")
            return "quitter"
        if contient(texte, MOTS_VEILLE):
            parler("Je repasse en veille.")
            return "veille"
        reponse = cerveau.repondre(texte)
        print("Jarvis :", reponse)
        parler(reponse)


cerveau = Cerveau()
parler("Systèmes en ligne.")

while True:
    reveil.attendre()
    parler("Oui ?")
    if conversation(cerveau) == "quitter":
        break