import sys
import os
import site


def is_venv():
    # if in venv, sys.prefix points to the program's root dir
    # if not, it points to the sys wide Python installation (/usr/local)
    if hasattr(sys, "base_prefix"):
        if sys.prefix != sys.base_prefix:
            return True
        else:
            return False
    else:
        return False


def print_outside_matrix():
    print("MATRIX STATUS: You're still plugged in")
    print("Current Python: " + sys.executable)
    print("Virtual Environment: None detected")
    print("")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("")
    print("To enter the construct, run:")
    print("python3 -m venv matrix_env")
    print("source matrix_env/bin/activate  # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows")
    print("")
    print("Then run this program again.")


def print_inside_matrix():
    env_path = sys.prefix
    env_name = os.path.basename(env_path)

    print("MATRIX STATUS: Welcome to the construct")
    print("Current Python: " + sys.executable)
    print("Virtual Environment: " + env_name)
    print("Environment Path: " + env_path)
    print("")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print("")

    site_packages_path = ""
    if hasattr(site, "getsitepackages"):
        packages_list = site.getsitepackages()
        if len(packages_list) > 0:
            site_packages_path = packages_list[0]

    if site_packages_path == "":
        python_version = "python" + str(sys.version_info.major) + "." + str(sys.version_info.minor)
        site_packages_path = os.path.join(env_path, "lib", python_version, "site-packages")

    print("Package installation path: " + site_packages_path)


def main():
    print("Welcome to the Real World of Data Engineering")
    print("")

    if is_venv() == True:
        print_inside_matrix()
    else:
        print_outside_matrix()


if __name__ == "__main__":
    main()