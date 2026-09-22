from pydantic import BaseModel


class CodebaseIndexRequest(BaseModel):
    project_path: str


class FileInfo(BaseModel):
    path: str
    extension: str
    size: int


class CodebaseIndexResponse(BaseModel):
    project_name: str
    file_count: int
    files: list[FileInfo]