# JARVIS : assistant vocal IA local

Un assistant vocal inspiré de JARVIS, 100 % gratuit et open source, qui tourne sur mon laptop (Ryzen 5, 16 Go de RAM, sans carte graphique dédiée). Projet d'apprentissage construit étape par étape et documenté en public.

## Ce qu'il sait faire (état actuel)
- Écouter au micro et s'arrêter automatiquement quand je finis ma phrase (faster-whisper)
- Réfléchir avec un modèle local (Ollama), **interchangeable en modifiant 3 lignes dans `.env`**
- Répondre à voix haute en français (Piper)
- Tenir une conversation avec mémoire du contexte
- Se fermer à la voix (« exit », « au revoir »,bye) ** aussi modifiable tu peux dire se que tu veux **

## Architecture
```
Micro -> oreilles.py -> cerveau.py -> voix.py -> Haut-parleur
                            ^
                         main.py
```
Chaque module est indépendant : on peut changer de modèle, de voix ou de reconnaissance vocale sans toucher au reste.

## Installation (Windows)
1. Installer Python 3.11+ et [Ollama](https://ollama.com), puis `ollama pull qwen2.5:3b`
2. Cloner le dépôt, puis dans son dossier :
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m piper.download_voices fr_FR-siwis-medium
```
3. Créer un fichier `.env` :
```
BRAIN_BASE_URL=http://localhost:11434/v1
BRAIN_MODEL=qwen2.5:3b
BRAIN_API_KEY=ollama
VOICE_MODEL=fr_FR-siwis-medium
```
4. Lancer : `python main.py`

## Feuille de route
- [x] Chat texte avec modèle local
- [x] Voix (Piper)
- [x] Écoute (Whisper) et conversation vocale
- [ ] Mot d'éveil modifiable
- [ ] Outils (heure, météo, ouvrir un site, minuteur...)
- [ ] Mémoire entre les sessions
- [ ] Interface visuelle

Suivi détaillé dans [docs/devlog.md](docs/devlog.md).