import git
import subprocess
from time import sleep
from os import environ


# subprocess.run(["/usr/bin/ssh-keyscan", "github.com", ">>", "~/.ssh/known_hosts"], shell=True)
HOME = environ['HOME']
print(f"{HOME}/.ssh/known_hosts")

f = open(f"{HOME}/.ssh/known_hosts", "a")
subprocess.call(["/usr/bin/ssh-keyscan", "github.com"], stdout=f)

while True:
    g = git.cmd.Git("/project")
    g.pull()
    sleep(300)
