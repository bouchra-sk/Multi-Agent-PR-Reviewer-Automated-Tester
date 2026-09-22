"""
Stockage simple en mémoire, partagé entre les endpoints.
Pour un portfolio project ça suffit ; en production on utiliserait
une vraie base de données (PostgreSQL, Redis, etc.).
"""

# Arborescence du projet indexé, par project_id (rempli par l'Agent 1)
FOLDER_TREES: dict[str, str] = {}