import webbrowser
from datetime import datetime
from urllib.parse import quote
import requests
import os

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
    
CODES_METEO = {
    0: "ciel dégagé", 1: "ciel plutôt dégagé", 2: "ciel partiellement nuageux",
    3: "ciel couvert", 45: "du brouillard", 48: "du brouillard givrant",
    51: "une légère bruine", 53: "de la bruine", 55: "une forte bruine",
    61: "une légère pluie", 63: "de la pluie", 65: "une forte pluie",
    71: "une légère neige", 73: "de la neige", 75: "une forte neige",
    80: "de légères averses", 81: "des averses", 82: "de fortes averses",
    95: "de l'orage", 96: "de l'orage avec grêle", 99: "de l'orage avec forte grêle",
}


def meteo(ville=""):
    ville = ville.strip() or os.getenv("VILLE", "")
    if not ville:
        return "Pour quelle ville ? Je peux aussi utiliser une ville par défaut dans le fichier de configuration."
    try:
        g = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": ville, "count": 1, "language": "fr"},
            timeout=8,
        ).json()
        if not g.get("results"):
            return f"Je ne trouve pas la ville {ville}."
        lieu = g["results"][0]
        m = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lieu["latitude"],
                "longitude": lieu["longitude"],
                "current": "temperature_2m,weather_code,wind_speed_10m",
            },
            timeout=8,
        ).json()["current"]
        temps = CODES_METEO.get(m["weather_code"], "un temps variable")
        return (
            f"À {lieu['name']}, il fait {round(m['temperature_2m'])} degrés, "
            f"avec {temps}. Le vent souffle à {round(m['wind_speed_10m'])} kilomètres par heure."
        )
    except Exception:
        return "Je n'arrive pas à joindre le service météo."