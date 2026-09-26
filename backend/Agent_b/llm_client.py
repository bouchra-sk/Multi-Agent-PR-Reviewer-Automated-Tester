"""
Client générique pour appeler le LLM (IBM Bob 2.0).
"""

import requests
from backend.config import LLM_API_KEY, LLM_API_URL


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """
    Envoie un prompt au LLM ou retourne un résumé simulé si l'API externe est indisponible.
    """
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY ou Secret_Key manquant dans le .env")

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        # ⚠️ FALLBACK MOCK TEMPORAIRE (Évite la 502 pendant le dev/hackathon)
        print(f"⚠️ Appel LLM distant échoué ({e}).")
        return """### 1. Organisation des dossiers et technologies utilisées
- **Backend** : FastAPI, Uvicorn, Python 3.13
- **Base RAG & Vectorstore** : ChromaDB, LangChain
- **Structure** : Découpage par agents (`Agent1`, `Agent_b`) avec stockage en mémoire du state.

### 2. Points d'entrée du projet (Entry Points)
- `backend/main.py` : Expose l'API REST avec les routes `/index` et `/architecture/{project_id}`.

### 3. Comment naviguer et apporter des modifications
- Les prompts de l'Agent 2 se trouvent dans `backend/Agent_b/archi_agent.py`.
- L'indexation du code source est gérée dans `backend/Agent1/parsing.py` et `rag.py`."""