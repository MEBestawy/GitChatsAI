from fastapi import FastAPI

app = FastAPI()

@app.post("/cloneRepo")
def clone_repo(repo_link: str):
    return {
        "repo_link": repo_link
    }

