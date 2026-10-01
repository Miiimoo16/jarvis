import re
from cerveau import Cerveau
from voix import parler
from oreilles import ecouter

MOTS_SORTIE = ("au revoir", "exit", "quitter", "quitte", "arrête toi", "éteins toi",'bye', 'stop', 'a plus tard', 'à plus', 'à bientôt', 'à la prochaine')


def veut_quitter(texte):
    propre = " " + re.sub(r"[^\w\s]", " ", texte.lower()) + " "
    propre = re.sub(r"\s+", " ", propre)
    return any(f" {mot} " in propre for mot in MOTS_SORTIE)


cerveau = Cerveau()
parler("Systèmes en ligne. Je vous écoute.")

while True:
    texte = ecouter()
    if not texte:
        continue
    print("Toi :", texte)
    if veut_quitter(texte):
        parler("À bientôt chef.")
        break
    reponse = cerveau.repondre(texte)
    print("Jarvis :", reponse)
    parler(reponse)