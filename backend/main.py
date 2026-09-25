"""
Point d'entrée FastAPI — Agent 1 : Indexing & Parsing Agent

Endpoints :
- POST /index          : upload d'un zip de projet -> extraction + chunking + indexation RAG
- GET  /health          : vérifie que le serveur tourne
- GET  /tree/{project}  : retourne l'arborescence du dernier projet indexé
"""

import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.Agent1.parsing import extract_zip, build_folder_tree, build_chunks
from backend.Agent1.rag import index_chunks
from backend.Agent_b.state import FOLDER_TREES
from backend.Agent_b.archi_agent import summarize_architecture
from backend.Agent3.qa_agent import answer_question

app = FastAPI(title="Codebase Indexing Agent")


class QuestionRequest(BaseModel):
    question: str

# Autorise Streamlit (généralement sur localhost:8501) à appeler ce backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/index")
async def index_project(file: UploadFile = File(...)):
    """
    Étape complète :
    1. Sauvegarde le zip uploadé sur disque
    2. L'extrait dans un dossier temporaire
    3. Construit l'arborescence + les chunks
    4. Indexe les chunks dans ChromaDB
    5. Retourne un résumé au frontend Streamlit
    """
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Merci d'uploader un fichier .zip")

    project_id = str(uuid.uuid4())[:8]
    temp_zip_path = f"./_upload_{project_id}.zip"

    # 1. Sauvegarde du zip reçu
    with open(temp_zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 2. Extraction
        extracted_path = extract_zip(temp_zip_path)

        # 3. Arborescence + chunking
        tree = build_folder_tree(extracted_path)
        chunks = build_chunks(extracted_path)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Aucun fichier de code source trouvé dans le zip.",
            )

        # 4. Indexation dans le RAG
        nb_indexed = index_chunks(project_id, chunks)

        FOLDER_TREES[project_id] = tree

        # 5. Réponse pour Streamlit
        return {
            "project_id": project_id,
            "nb_files_indexed": len({c["metadata"]["file_path"] for c in chunks}),
            "nb_chunks_indexed": nb_indexed,
            "folder_tree": tree,
        }

    finally:
        # Nettoyage du zip temporaire
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)


@app.get("/tree/{project_id}")
def get_tree(project_id: str):
    tree = FOLDER_TREES.get(project_id)
    if tree is None:
        raise HTTPException(status_code=404, detail="Projet inconnu")
    return {"project_id": project_id, "folder_tree": tree}


@app.post("/architecture/{project_id}")
def get_architecture_summary(project_id: str):
    """
    Agent 2 : Architecture Summarizer Agent.
    Doit être appelé APRÈS /index — il s'appuie sur le RAG déjà construit
    par l'Agent 1 pour ce project_id.
    """
    tree = FOLDER_TREES.get(project_id)
    if tree is None:
        raise HTTPException(
            status_code=404,
            detail="Projet inconnu — indexe-le d'abord via POST /index.",
        )

    try:
        summary = summarize_architecture(project_id, tree)
    except RuntimeError as e:
        # Cas où LLM_API_KEY / LLM_API_URL ne sont pas configurés dans .env
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur lors de l'appel au LLM : {e}")

    return {"project_id": project_id, "architecture_summary": summary}


@app.post("/ask/{project_id}")
def ask_question(project_id: str, payload: QuestionRequest):
    """Agent 3 : répond à une question sur le codebase indexé."""
    if project_id not in FOLDER_TREES:
        raise HTTPException(
            status_code=404,
            detail="Projet inconnu — indexe-le d'abord via POST /index.",
        )

    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="La question ne peut pas être vide.")

    try:
        answer = answer_question(project_id, question)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur lors de l'appel au LLM : {e}") from e

    return {
        "project_id": project_id,
        "question": question,
        "answer": answer,
    }