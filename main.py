import git
import subprocess
from time import sleep

subprocess.run(["/usr/bin/ssh-keyscan" "github.com" ">>" "~/.ssh/known_hosts"])

while True:
    sleep(300)
