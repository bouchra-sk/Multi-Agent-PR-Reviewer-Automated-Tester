from __future__ import annotations

import re
from pathlib import Path


class OnboardingService:
    """Build a local searchable code index without requiring an external API key."""

    supported_extensions = {".py", ".js", ".ts", ".tsx", ".java", ".go", ".md"}

    def __init__(self) -> None:
        self.project_path: Path | None = None
        self.chunks: list[dict[str, str | int]] = []

    def index_project(self, project_path: str) -> dict[str, int | str]:
        root = Path(project_path).resolve()
        if not root.is_dir():
            raise ValueError("Project path is not a directory")

        ignored = {".git", ".venv", "venv", "agent", "__pycache__", "node_modules", ".idea", ".vscode"}
        chunks: list[dict[str, str | int]] = []
        for file_path in root.rglob("*"):
            if not file_path.is_file() or file_path.suffix.lower() not in self.supported_extensions:
                continue
            if any(part in ignored for part in file_path.parts):
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            lines = content.splitlines()
            for start in range(0, len(lines), 80):
                text = "\n".join(lines[start:start + 80]).strip()
                if text:
                    chunks.append({
                        "path": str(file_path.relative_to(root)),
                        "start_line": start + 1,
                        "end_line": min(start + 80, len(lines)),
                        "content": text,
                    })

        self.project_path = root
        self.chunks = chunks
        return {
            "project_name": root.name,
            "file_count": len({chunk["path"] for chunk in chunks}),
            "chunk_count": len(chunks),
        }

    def search(self, question: str, limit: int = 5) -> list[dict[str, str | int]]:
        terms = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]+", question.lower()))
        scored = []
        for chunk in self.chunks:
            searchable = f"{chunk['path']} {chunk['content']}".lower()
            score = sum(searchable.count(term) for term in terms)
            if score:
                scored.append((score, chunk))
        return [chunk for _, chunk in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]

    def architecture_summary(self) -> dict[str, object]:
        if self.project_path is None:
            raise ValueError("No codebase has been indexed")
        files = sorted({str(chunk["path"]) for chunk in self.chunks})
        entry_points = [
            path for path in files
            if Path(path).name in {"main.py", "app.py", "__main__.py"}
        ]
        return {
            "project_name": self.project_path.name,
            "file_count": len(files),
            "technologies": sorted({Path(path).suffix for path in files}),
            "entry_points": entry_points,
            "folders": sorted({str(Path(path).parent) for path in files if str(Path(path).parent) != "."}),
            "next_step": "Use /api/v1/onboarding/ask-copilot to locate relevant code before making changes.",
        }


onboarding_service = OnboardingService()