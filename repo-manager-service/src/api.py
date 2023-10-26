from fastapi import FastAPI
from config import CLONED_PROJECTS_BASE_DIRECTORY
from utils.utils import match_github_repo_info, clone_github_repo, save_repo_embeddings
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
	return {}

@app.put("/parseGithubRepo")
def parse_github_repo(repo_link: str):
    SUCCESS_OUTPUT = {"result": "Success!"}

    # get username and project name from url
    match = match_github_repo_info(repo_link)
    username, project_name = match.group("username"), match.group("project_name")

    # clone project in directory_path
    project_directory_path = (
        f"{CLONED_PROJECTS_BASE_DIRECTORY}/{username}/{project_name}/"
    )

    if not clone_github_repo(username, project_name, project_directory_path):
        return SUCCESS_OUTPUT

    save_repo_embeddings(username, project_name, project_directory_path)
    return SUCCESS_OUTPUT
