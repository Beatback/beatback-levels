from subprocess import run, PIPE
from os import environ

REPO = environ.get("REPO")
PR = environ.get("PR")
PR_AUTHOR = environ.get("PR_AUTHOR")

ALLOWED_DIRS = [
    "levels",
    "info"
]

exec_shell = lambda cmd: run(cmd, stdout=PIPE).stdout.decode("utf-8").rstrip()

changed_files = exec_shell(["gh", "pr", "diff", PR, "--name-only", "-R", REPO]).splitlines()
if not all([any([not i.startswith(j+"/") for j in ALLOWED_DIRS]) for i in changed_files]):
    print("File changes to a prohibited directory!")
    exit(1)

for file in changed_files:
    file_author = exec_shell(["gh", "api", f"repos/{REPO}/commits?path={file}", "--jq", ".[-1].author.login"])
    if file_author and PR_AUTHOR != file_author:
        print("Editing a file from a different author!")
        exit(1)