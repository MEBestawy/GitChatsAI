from fastapi import FastAPI
from utils.utils import match_github_repo_info, clone_github_repo

app = FastAPI()


@app.put("/parseGithubRepo")
def parse_github_repo(repo_link: str):
    SUCCESS_OUTPUT = {"result": "Success!"}

    # get username and project name from url
    match = match_github_repo_info(repo_link)
    username, project_name = match.group("username"), match.group("project_name")

    # clone project in
    directory_path = f"{username}/{project_name}/"
    clone_github_repo(username, project_name, directory_path)

    # TODO: Parse & Embed docs from code

    return SUCCESS_OUTPUT
