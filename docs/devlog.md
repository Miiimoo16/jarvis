# Devlog

## 1er octobre 2026 : première conversation vocale complète
**Fait :** cerveau local (Ollama), voix (Piper), oreilles (Whisper), boucle vocale, mots de sortie.

**Problèmes et solutions :**
- Fichiers vides : le code n'était pas enregistré. Solution : activer l'enregistrement automatique de VS Code.
- Voix qui massacrait les accents : problème d'encodage entre Python et Piper sous Windows. Solution : forcer l'UTF-8.
- Fin des phrases coupée : ajout d'un silence en fin de son.
- Dépôt GitHub trop lourd : le dossier `venv` avait été publié par erreur. Solution : remplir le `.gitignore` avant le premier `git add`, puis repartir d'un historique propre.

**Appris :** un module par fichier, et la config dans `.env`, rend les changements faciles.

**Prochaine étape :** mot d'éveil modifiable.