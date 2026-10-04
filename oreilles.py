import numpy as np
import sounddevice as sd
from collections import deque
from faster_whisper import WhisperModel

SR = 16000
BLOC = 0.1          # on écoute par tranches de 0,1 seconde
ATTENTE_MAX = 8     # abandon si tu ne dis rien pendant 8 secondes
PAROLE_MAX = 20     # durée maximale d'une phrase
SEUIL = 0.006       # plus sensible : les mots dits doucement sont captés
FIN_SILENCE = 1.8   # il attend plus longtemps avant de te couper
AVANT = 0.5         # demi-seconde conservée avant le début de ta voix
modele = WhisperModel("small", device="cpu", compute_type="int8")
PROMPT = "Conversation en français avec Jarvis, un assistant vocal. Ouvre YouTube. Quelle heure est-il ? Ouvre Google."


def enregistrer():
    taille = int(BLOC * SR)
    avant = deque(maxlen=int(AVANT / BLOC))
    morceaux = []
    parle = False
    silence = 0.0
    attente = 0.0
    with sd.InputStream(samplerate=SR, channels=1, dtype="float32", blocksize=taille) as flux:
        while True:
            data, _ = flux.read(taille)
            data = data.flatten()
            niveau = np.sqrt(np.mean(data ** 2))
            if not parle:
                if niveau > SEUIL:
                    parle = True
                    morceaux = list(avant)
                    morceaux.append(data)
                else:
                    avant.append(data)
                    attente += BLOC
                    if attente >= ATTENTE_MAX:
                        return None
            else:
                morceaux.append(data)
                if niveau > SEUIL:
                    silence = 0.0
                else:
                    silence += BLOC
                if silence >= FIN_SILENCE or len(morceaux) * BLOC >= PAROLE_MAX:
                    break
    return np.concatenate(morceaux)

def ecouter():
    print("Je t'écoute...")
    audio = enregistrer()
    if audio is None:
        return ""
    segments, _ = modele.transcribe(
        audio, language="fr", beam_size=5, vad_filter=True, initial_prompt=PROMPT
    )
    return " ".join(s.text for s in segments).strip()


if __name__ == "__main__":
    print("J'ai compris :", ecouter())