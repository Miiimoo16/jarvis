import os
import re
import unicodedata
import difflib
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from oreilles import enregistrer

load_dotenv()

modele_reveil = WhisperModel("tiny", device="cpu", compute_type="int8")


def normaliser(texte):
    """Minuscules, sans accents ni ponctuation."""
    texte = unicodedata.normalize("NFD", texte.lower())
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", texte)


def mots_eveil():
    brut = os.getenv("WAKE_WORDS", "jarvis")
    return [normaliser(m).strip() for m in brut.split(",") if m.strip()]


def contient_le_mot(texte):
    seuil = float(os.getenv("WAKE_SENSITIVITY", "0.75"))
    texte = normaliser(texte)
    for mot in mots_eveil():
        if mot in texte:
            return True
        for entendu in texte.split():
            if difflib.SequenceMatcher(None, entendu, mot).ratio() >= seuil:
                return True
    return False


def attendre():
    print("En veille... dis ton mot d'éveil.")
    while True:
        audio = enregistrer()
        if audio is None:
            continue
        segments, _ = modele_reveil.transcribe(
            audio, language="fr", beam_size=1, vad_filter=True
        )
        texte = " ".join(s.text for s in segments).strip()
        print("(entendu :", texte, ")")
        if texte and contient_le_mot(texte):
            return