import git
import subprocess
import os
from time import sleep

# Environment variables
HOME = os.environ['HOME']
GIT_REPO = os.environ.get("GIT_REPO", "git@github.com:cookiefan2012/KeyToDaLock.git")
BRANCH = os.environ.get("GIT_BRANCH", "master")
PROJECT_DIR = "/project"

# Add GitHub to known_hosts
print(f"{HOME}/.ssh/known_hosts")
with open(f"{HOME}/.ssh/known_hosts", "w") as f:
    subprocess.call(["/usr/bin/ssh-keyscan", "github.com"], stdout=f)

# Ensure the project directory is ready for cloning or pulling
if os.path.exists(PROJECT_DIR):
    # Check if the directory contains files, including "lost+found"
    if "lost+found" in os.listdir(PROJECT_DIR) and len(os.listdir(PROJECT_DIR)) == 1:
        print("Project directory only contains 'lost+found'. Proceeding with clone...")
        subprocess.run(["rm", "-rf", f"{PROJECT_DIR}/lost+found"], check=True)

    try:
        g = git.Repo(PROJECT_DIR)
        if g.remotes.origin.url != GIT_REPO:
            print(f"Mismatch in repository URL. Found {g.remotes.origin.url}, expected {GIT_REPO}.")
            raise ValueError("Invalid repository URL.")
        print("Repository already exists. Pulling latest changes...")

        # Reset to the remote branch to ensure a clean state
        g.git.fetch("--all")
        g.git.reset("--hard", f"origin/{BRANCH}")
    except (git.exc.InvalidGitRepositoryError, ValueError):
        print("Existing directory is not a valid repository. Cleaning up...")
        subprocess.run(["rm", "-rf", f"{PROJECT_DIR}/*"], check=True)
        subprocess.run(["git", "clone", "--branch", BRANCH, GIT_REPO, PROJECT_DIR], check=True)
else:
    print("Cloning repository...")
    subprocess.run(["git", "clone", "--branch", BRANCH, GIT_REPO, PROJECT_DIR], check=True)

# Start the sync loop
while True:
    g = git.cmd.Git(PROJECT_DIR)
    try:
        g.pull()
    except git.exc.GitCommandError as e:
        print(f"Error during pull: {e}")
    sleep(300)
