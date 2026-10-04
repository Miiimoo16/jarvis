import webbrowser
from datetime import datetime
from urllib.parse import quote

# Raccourcis pratiques (ce n'est PAS une restriction)
RACCOURCIS = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
    "whatsapp": "https://web.whatsapp.com",
    "wikipedia": "https://fr.wikipedia.org",
    "chatgpt": "https://chatgpt.com",
    "claude": "https://claude.ai",
    "twitter": "https://x.com",
    "tiktok": "https://www.tiktok.com",
    "drive": "https://drive.google.com",
}

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def heure_actuelle():
    n = datetime.now()
    jour = "premier" if n.day == 1 else n.day
    heure = f"{n.hour} heures" + (" pile" if n.minute == 0 else f" {n.minute}")
    return f"Il est {heure}, nous sommes {JOURS[n.weekday()]} {jour} {MOIS[n.month - 1]} {n.year}."


def ouvrir_site(nom):
    cle = nom.lower().strip()
    compact = cle.replace(" ", "")  # « chat gpt » devient « chatgpt »
    if compact in RACCOURCIS:
        url = RACCOURCIS[compact]
    elif "." in cle and " " not in cle:
        url = cle if cle.startswith(("http://", "https://")) else "https://" + cle
    else:
        url = "https://www.google.com/search?q=" + quote(nom)
        webbrowser.open(url)
        return f"Je lance une recherche pour {nom}."
    if not url.startswith(("http://", "https://")):
        return "Je n'ouvre que des adresses web."
    webbrowser.open(url)
    return f"J'ouvre {nom}."


# "direct": True = la phrase renvoyée est dite telle quelle, sans que le modèle la réécrive
OUTILS = {
    "heure_actuelle": {
        "fonction": heure_actuelle,
        "direct": True,
        "description": "Donne l'heure et la date actuelles.",
        "parametres": {"type": "object", "properties": {}},
    },
    "ouvrir_site": {
        "fonction": ouvrir_site,
        "direct": True,
        "description": "Ouvre un site web. À appeler pour TOUTE demande d'ouverture "
        "de site, quel que soit le site demandé.",
        "parametres": {
            "type": "object",
            "properties": {
                "nom": {"type": "string", "description": "Nom du site, ex. youtube"}
            },
            "required": ["nom"],
        },
    },
}


def schemas():
    """Description des outils, au format attendu par l'API."""
    return [
        {
            "type": "function",
            "function": {
                "name": nom,
                "description": outil["description"],
                "parameters": outil["parametres"],
            },
        }
        for nom, outil in OUTILS.items()
    ]


def est_direct(nom):
    return OUTILS.get(nom, {}).get("direct", False)


def executer(nom, arguments):
    if nom not in OUTILS:
        return "Outil inconnu."
    try:
        return OUTILS[nom]["fonction"](**arguments)
    except Exception as erreur:
        return f"Erreur : {erreur}"