from fastapi import FastAPI
from config import CLONED_PROJECTS_BASE_DIRECTORY
from utils.processor import gitProcessor
from utils.utils import match_github_repo_info
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

@app.put("/query")
def askme(query: str , repo_link: str):

    match = match_github_repo_info(repo_link)
    username, project_name = match.group("username"), match.group("project_name")

    # clone project in directory_path
    project_directory_path = (
        f"{CLONED_PROJECTS_BASE_DIRECTORY}/{username}/{project_name}/"
    )
    processor_instance = gitProcessor()

    result = processor_instance.processing(f"{username}-{project_name}", query)

    return result 
    