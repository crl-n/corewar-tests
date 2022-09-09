#!/usr/bin/env python3

import os
from subprocess import run, PIPE

def check_basic_stuff(dir):
    files = [f for f in os.listdir(dir)]
    if "Makefile" not in files:
        print("No Makefile found")
    if "author" not in files:
        print("No author file found")

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
    '''Looks for a Corewar directory. The script's sibling and parent directories are searched,
    as well as the script directory itself.'''
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(script_dir)
    print('script dir', script_dir)
    print('parent dir', parent_dir)
    dirs = [f.path for f in os.scandir(parent_dir) if f.is_dir()]
    dirs.append(script_dir)
    dirs.append(parent_dir)

    print("Checking if any of the following directories are a Corewar-directory:\n", dirs)
    for dir in dirs:
        if is_corewar_root_dir(dir):
            return dir
    return None

def main():
    project_dir = find_project_dir()
    if project_dir is None:
        print("Error: Couldn't locate Corewar directory")
    print("Corewar directory found:", project_dir)
    check_basic_stuff(project_dir)

if __name__ == '__main__':
    main()
