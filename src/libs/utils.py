from langchain_community.document_loaders import DirectoryLoader, TextLoader
import json

from src.libs.constants import DOCUMENTATION_DIR, PORTFOLIO_FILE, LOGS_FILE


def get_json():
    with open(PORTFOLIO_FILE, encoding="utf-8") as f:
        return json.load(f)

def get_documents():
    dir_loader = DirectoryLoader(
            path=str(DOCUMENTATION_DIR),
            glob="*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
    return dir_loader.load()

def get_logs():
    with open(LOGS_FILE, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        return contenido.splitlines()