from shutil import which
from utils import *
import os

def main():
    required_commands = ["gcc", "make", "git"]
    missing_commands = []

    is_fedora_atomic = False

    if which("rpm-ostree") is not None:
        is_fedora_atomic = True

    for command in required_commands:
        if which(command) is None:
            missing_commands.append(command)
            print(f"{bcolors.WARNING}Command '{command}' not found{bcolors.ENDC}")

    if not missing_commands:
            print(f"{bcolors.OKGREEN}All required commands found in PATH{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}Missing commands: {", ".join(str(x) for x in missing_commands)}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}{bcolors.BOLD}Please install the missing packages before proceeding{bcolors.ENDC}")

    kernel_version = os.popen("uname -r").read().strip()
    kernel_headers_path = f"/lib/modules/{kernel_version}/build"
    if os.path.exists(kernel_headers_path):
        print(f"{bcolors.OKGREEN}Kernel headers found at {kernel_headers_path}{bcolors.ENDC}")
    else:
        if is_fedora_atomic:
            missing_commands.append(f"kernel-modules-internal-{kernel_version}")
            missing_commands.append(f"kernel-devel-{kernel_version}")
        else:
            missing_commands.append("kernel headers (search for your distro's package)")
        print(f"{bcolors.FAIL}Kernel headers not found at {kernel_headers_path}{bcolors.ENDC}")

    if is_fedora_atomic:
        print(f"{bcolors.OKBLUE}Fedora Atomic detected{bcolors.ENDC}")
        if missing_commands:
            pkgs_inst = input("Would you like to install the required packages? [Y/n] ")
            if check_input(pkgs_inst) == False:
                print(f"{bcolors.FAIL}Invalid input, exiting...{bcolors.ENDC}")
                exit(1)
            elif pkgs_inst.lower() in ["n", "no"]:
                print(f"{bcolors.FAIL}Exiting...{bcolors.ENDC}")
                exit(1)
            else:
                print(f"This command will be executed: {bcolors.WARNING}{bcolors.BOLD}rpm-ostree install {" ".join(str(x) for x in missing_commands)}{bcolors.ENDC}")
                print(f"{bcolors.WARNING}Please note that this will require a reboot{bcolors.ENDC}")
                pkgs_inst2 = input("Would you like to proceed? [Y/n] ")
                if check_input(pkgs_inst2) == False:
                    print(f"{bcolors.FAIL}Invalid input, exiting...{bcolors.ENDC}")
                    exit(1)
                elif pkgs_inst2.lower() in ["n", "no"]:
                    print(f"{bcolors.FAIL}Exiting...{bcolors.ENDC}")
                    exit(1)
                else:
                    os.system(f"rpm-ostree install {" ".join(str(x) for x in missing_commands)}")
                    print(f"{bcolors.OKGREEN}Packages installed successfully{bcolors.ENDC}")
                    print(f"{bcolors.WARNING}Please reboot your system for the changes to take effect!{bcolors.ENDC}")
        else:
            print(f"{bcolors.OKCYAN}Requirements met, no further action needed{bcolors.ENDC}")
            return True
    elif missing_commands:
        print(f"{bcolors.FAIL}{bcolors.BOLD}Please install the missing packages before proceeding{bcolors.ENDC}")
        if __name__ == "__main__":
            exit(1)
        else:
            return False
    elif not missing_commands:
        print(f"{bcolors.OKCYAN}Requirements met, no further action needed{bcolors.ENDC}")
        return True

if __name__ == "__main__":
    main()
