import re

MOTS_QUITTER = ("exit", "exite", "quitter", "quitte")
MOTS_VEILLE = ("au revoir", "à plus tard",'pause')


def contient(texte, mots):
    propre = " " + re.sub(r"[^\w\s]", " ", texte.lower()) + " "
    propre = re.sub(r"\s+", " ", propre)
    return any(f" {mot} " in propre for mot in mots)

def extraire_ouverture(texte):
    """Si la phrase est « ouvre X », renvoie X. Sinon renvoie None."""
    m = re.match(
        r"^\s*(?:ouvre|ouvrez|ouvrir|lance|lancez)\s+(?:moi\s+)?"
        r"(?:le site de |le site du |le site |la page |le |la |l'|l’|les )?([^.!?]+)",
        texte,
        re.IGNORECASE,
    )
    return m.group(1).strip() if m else None