import os
from dotenv import load_dotenv

load_dotenv()

# Environment-specific settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
CLONED_PROJECTS_BASE_DIRECTORY = os.getenv("CLONED_PROJECTS_BASE_DIRECTORY")

# File extensions to be parsed in code repos
FILE_EXTENSIONS = [
    "txt",
    "md",
    "markdown",
    "rst",
    "rs",
    "py",
    "js",
    "java",
    "c",
    "cpp",
    "cs",
    "go",
    "rb",
    "php",
    "scala",
    "html",
    "htm",
    "xml",
    "json",
    "yaml",
    "yml",
    "ini",
    "toml",
    "cfg",
    "conf",
    "sh",
    "bash",
    "css",
    "scss",
    "sql",
    "gitignore",
    "dockerignore",
    "editorconfig",
    "ipynb",
]
