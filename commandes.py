import re

MOTS_QUITTER = ("exit", "exite", "quitter", "quitte")
MOTS_VEILLE = ("au revoir", "à plus tard",'pause')


def contient(texte, mots):
    propre = " " + re.sub(r"[^\w\s]", " ", texte.lower()) + " "
    propre = re.sub(r"\s+", " ", propre)
    return any(f" {mot} " in propre for mot in mots)