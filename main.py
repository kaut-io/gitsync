import os
import git
import subprocess
from time import sleep
from os import environ

HOME = environ['HOME']
GIT_REPO = environ.get("GIT_REPO")  # Set this environment variable in your Kubernetes config
BRANCH = environ.get("GIT_BRANCH", "main")  # Optional: Defaults to "main"

project_dir = "/project"
known_hosts_file = f"{HOME}/.ssh/known_hosts"

# Ensure GitHub is in known_hosts
with open(known_hosts_file, "w") as f:
    subprocess.call(["/usr/bin/ssh-keyscan", "github.com"], stdout=f)
print(f"Added GitHub to {known_hosts_file}")

# Clone the repository if it doesn't exist
if not os.path.isdir(os.path.join(project_dir, ".git")):
    print("Cloning repository...")
    subprocess.run(["git", "clone", "--branch", BRANCH, GIT_REPO, project_dir], check=True)
else:
    print("Repository already exists. Skipping clone.")

# Periodic pull updates
while True:
    try:
        g = git.cmd.Git(project_dir)
        print("Pulling latest changes...")
        g.pull()
        print("Git pull completed successfully.")
    except Exception as e:
        print(f"Error during git pull: {e}")
    sleep(300)
