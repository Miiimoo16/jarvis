from cerveau import Cerveau
from voix import parler
from oreilles import ecouter
from commandes import (
    MOTS_QUITTER, MOTS_VEILLE, contient, extraire_ouverture, extraire_meteo,
)
from outils import ouvrir_site, meteo
import reveil


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
        site = extraire_ouverture(texte)
        ville = extraire_meteo(texte)
        if site:
            reponse = ouvrir_site(site)
            print("[direct] ouvrir_site", site, "->", reponse)
        elif ville is not None:
            reponse = meteo(ville)
            print("[direct] meteo", repr(ville), "->", reponse)
        else:
            reponse = cerveau.repondre(texte)
            print("Jarvis :", reponse)
        parler(reponse)


cerveau = Cerveau()
parler("Systèmes en ligne.")

while True:
    if reveil.attendre() == "quitter":
        parler("À bientôt.")
        break
    parler("Oui ?")
    if conversation(cerveau) == "quitter":
        break