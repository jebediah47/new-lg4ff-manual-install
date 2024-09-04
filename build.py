from utils import *
import prerequisites
import subprocess
import os

prerequisites_satisfied = prerequisites.main()

if not prerequisites_satisfied:
    print("Prerequisites not satisfied, exiting...")
    exit(1)

username = os.popen("whoami").read().strip()

if not os.path.exists(f"/home/{username}/.local/new-lg4ff/"):
    os.makedirs(f"/home/{username}/.local/new-lg4ff/")
if not os.path.exists(f"/home/{username}/.local/new-lg4ff/build"):
    os.makedirs(f"/home/{username}/.local/new-lg4ff/build")

repo_path = f"/home/{username}/.local/new-lg4ff/new-lg4ff-src"
if not os.path.exists(repo_path):
    os.system(f"git clone https://github.com/berarma/new-lg4ff {repo_path}")
os.chdir(repo_path)

local_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode('utf-8')
os.system("git fetch")
remote_commit_hash = subprocess.check_output(["git", "rev-parse", "origin/master"]).strip().decode('utf-8')

if local_commit_hash != remote_commit_hash:
    user_input = input("There are updates available in the repository. Update? [Y/n]: ")
    if validate_yn(user_input):
        os.chdir(f"/home/{username}/.local/new-lg4ff/")
        os.rmdir("new-lg4ff-src")
        os.system(f"git clone https://github.com/berarma/new-lg4ff {repo_path}")

build_dir = f"/home/{username}/.local/new-lg4ff/build"

os.system("make")

if not os.path.exists(build_dir):
    os.makedirs(build_dir)

if not os.path.exists(f"{build_dir}/current"):
    os.makedirs(f"{build_dir}/current")

os.system(f"cp /home/cllupo/Downloads/new-lg4ff/hid-logitech-new.ko {build_dir}/{local_commit_hash}")

if os.path.exists(f"{build_dir}/{local_commit_hash}"):
    os.symlink(f"{build_dir}/{local_commit_hash}/hid-logitech-new.ko", f"{build_dir}/current/hid-logitech-new.ko")
    print(f"Created symlink: build/{local_commit_hash}/logitech-hid-new.ko -> build/current/logitech-hid-new.ko")
