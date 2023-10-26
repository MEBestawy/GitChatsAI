from fastapi import HTTPException
from config import FILE_EXTENSIONS, QDRANT_URL
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.qdrant import Qdrant
import re, os, subprocess


def match_github_repo_info(repo_link: str):
    """
    Parses the given github repo URL (with or without the base url) and returns the Match object.

    Raises a HTTPException if the provided <repo_link> could not be parsed.
    """
    match = re.match(
        r"(?:https?://github\.com/)?(?P<username>[^/]+)/(?P<project_name>[^/]+)",
        repo_link,
    )
    if not match:
        raise HTTPException(
            status_code=400,
            detail="Could not parse github repo link. Are you sure this url links to a repo?",
        )

    return match


def clone_github_repo(username: str, project_name: str, target_directory_path: str):
    """
    Clones the Github repo named <project_name> under <username>'s account into <target_directory_path>.

    Returns a bool indicating whether it cloned a new repo or not.
    """
    if os.path.exists(target_directory_path):
        return False

    clone_command = [
        "git",
        "clone",
        f"https://github.com/{username}/{project_name}",
        target_directory_path,
    ]
    result = subprocess.run(clone_command, capture_output=True, text=True)

    if result.returncode != 0:
        print(result)
        raise HTTPException(
            status_code=404,
            detail="Error cloning the repository. Are you sure this url links to a repo?",
        )
    return True


def save_repo_embeddings(username: str, project_name: str, directory_path: str):
    documents = []
    for ext in FILE_EXTENSIONS:
        documents += DirectoryLoader(
            directory_path,
            glob=f"**/*.{ext}",
            recursive=True,
            use_multithreading=True,
            loader_cls=TextLoader,
            silent_errors=True,
            loader_kwargs={"autodetect_encoding": True},
            show_progress=False,
        ).load()

    embeddings = OpenAIEmbeddings()

    Qdrant.from_documents(
        documents,
        embeddings,
        api_key="QFy82_cm889Hbft8rGp3fAezDY6kN_b8KTi_a926DRq8OfVpbX6N_Q",
        url=QDRANT_URL,
        collection_name=f"{username}-{project_name}",
    )
