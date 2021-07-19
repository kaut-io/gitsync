import git
import subprocess
from time import sleep

subprocess.run(["/usr/bin/ssh-keyscan", "github.com", ">>", "~/.ssh/known_hosts"], shell=True)

while True:
    g = git.cmd.Git("/project")
    g.pull()
    sleep(300)
