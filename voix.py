import os
import subprocess
import sys
import time
import wave
import winsound
from dotenv import load_dotenv

load_dotenv()

FICHIER = "reponse.wav"


def ajouter_silence(fichier, secondes=0.6):
    """Ajoute du silence à la fin du son pour éviter qu'il soit coupé."""
    with wave.open(fichier, "rb") as f:
        params = f.getparams()
        frames = f.readframes(f.getnframes())
    silence = b"\x00" * (int(params.framerate * secondes) * params.sampwidth * params.nchannels)
    with wave.open(fichier, "wb") as f:
        f.setparams(params)
        f.writeframes(frames + silence)


def parler(texte):
    modele = os.getenv("VOICE_MODEL", "fr_FR-siwis-medium")
    env = {**os.environ, "PYTHONUTF8": "1"}
    subprocess.run(
        [sys.executable, "-m", "piper", "-m", modele, "-f", FICHIER],
        input=texte,
        text=True,
        encoding="utf-8",
        env=env,
        check=True,
    )
    ajouter_silence(FICHIER)
    winsound.PlaySound(FICHIER, winsound.SND_FILENAME)
    time.sleep(0.3)