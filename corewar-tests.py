#!/usr/bin/env python3

import os
from subprocess import run, Popen, PIPE

def check_basic_stuff(dir: str):
    files = [f for f in os.listdir(dir) if os.path.isfile(f)]
    if "Makefile" not in files:
        print("No Makefile")
    if "author" not in files:
        print("No Makefile")

def is_corewar_root_dir(dir: str):
    '''Checks if dir has a Makefile that mentions Corewar. If it does, it is interpreted
    as an indication of that the dir is a root directory of a Corewar project.'''
    files = os.listdir(dir)
    for file in files:
        if file == "Makefile":
            result = run(["grep", "corewar", os.path.abspath(os.path.join(dir, "Makefile"))], stdout = PIPE)
            if result.returncode == 0:
                return True
    return False

def find_project_dir():
    '''Checks if cwd, cwd's parent directory or any of cwd's sibling directories are a corewar directory.'''
    dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    dirs.append(os.getcwd())
    dirs.append(os.path.abspath(os.pardir))

    print("Checking if any of the following directories are a Corewar-directory:\n", dirs)
    for dir in dirs:
        if is_corewar_root_dir(dir):
            return dir
    return None

def main():
    project_dir = find_project_dir()
    print("Corewar directory found:", project_dir)

if __name__ == '__main__':
    main()
