import prerequisites
import subprocess
import os

prerequisites_satisfied = prerequisites.main()

if not prerequisites_satisfied:
    print("Prerequisites not satisfied, exiting...")
    exit(1)

username = os.popen("whoami").read().strip()

os.system(f"mkdir -p /home/{username}/.local/new-lg4ff/")
os.system(f"mkdir -p /home/{username}/.local/new-lg4ff/build")

repo_path = f"/home/{username}/.local/new-lg4ff/new-lg4ff-src"
if not os.path.exists(repo_path):
    os.system(f"git clone https://github.com/berarma/new-lg4ff {repo_path}")

os.chdir(repo_path)

local_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode('utf-8')

os.system("git fetch")
remote_commit_hash = subprocess.check_output(["git", "rev-parse", "origin/master"]).strip().decode('utf-8')

if local_commit_hash != remote_commit_hash:
    user_input = input("There are updates available in the repository. Do you want to pull the changes? (yes/no): ")
    if user_input.lower() == 'yes':
        os.system("git pull")

build_dir = f"/home/{username}/.local/new-lg4ff/build/{local_commit_hash}"

os.system("make")

if not os.path.exists(build_dir):
    os.makedirs(build_dir)

os.system(f"cp /home/cllupo/Downloads/new-lg4ff/hid-logitech-new.ko {build_dir}/")
