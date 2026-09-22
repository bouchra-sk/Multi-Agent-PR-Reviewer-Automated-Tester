import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORTS DES AUTRES FICHIERS DU PROJET ---
from backend.Agent1.parsing import extract_zip, build_folder_tree, build_chunks
from backend.Agent1.rag import index_chunks
from backend.Agent1.indexing_agent import IndexingAgent  # Import de ton agent d'indexation

app = FastAPI(title="Codebase Indexing Agent")

# Instanciation de l'agent
indexing_agent = IndexingAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LAST_TREE_BY_PROJECT: dict[str, str] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/index")
async def index_project(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Merci d'uploader un fichier .zip")

    project_id = str(uuid.uuid4())[:8]
    temp_zip_path = f"./_upload_{project_id}.zip"

    # 1. Sauvegarde du fichier zip temporaire
    with open(temp_zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 2. Extraction du zip (depuis parsing.py)
        extracted_path = extract_zip(temp_zip_path)

        # 3. Arborescence + Chunking (depuis parsing.py)
        tree = build_folder_tree(extracted_path)
        chunks = build_chunks(extracted_path)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Aucun fichier de code source trouvé dans le zip.",
            )

        # 4. Indexation vectorielle dans ChromaDB (depuis rag.py)
        nb_indexed = index_chunks(project_id, chunks)

        LAST_TREE_BY_PROJECT[project_id] = tree

        # 5. Réponse envoyée au Frontend (Streamlit)
        return {
            "project_id": project_id,
            "nb_files_indexed": len({c["metadata"]["file_path"] for c in chunks}),
            "nb_chunks_indexed": nb_indexed,
            "folder_tree": tree,
        }

    finally:
        # Nettoyage du zip temporaire sur le disque
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)


@app.get("/tree/{project_id}")
def get_tree(project_id: str):
    tree = LAST_TREE_BY_PROJECT.get(project_id)
    if tree is None:
        raise HTTPException(status_code=404, detail="Projet inconnu")
    return {"project_id": project_id, "folder_tree": tree}