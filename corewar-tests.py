#!/usr/bin/env python3

import os
import sys
from library import *
from check_basic import check_basic_stuff
from check_asm import check_assembler
from check_vm import check_virtual_machine
from subprocess import run, PIPE, DEVNULL
from functools import reduce

def retrieve_resources():
    if input(red("The official 42 Corewar resources could not be found.") + " Would you like to download them from intra.42.fr? (yes/no) ") in ['y', 'yes', 'Y' , 'Yes']:
        curl_result = run(['curl', '--remote-name', 'https://projects.intra.42.fr/uploads/document/document/1170/vm_champs.tar'], stdout = DEVNULL, stderr = DEVNULL)
        if curl_result.returncode != 0:
            print(red("Error: Could not download resources. Check you network connection."))
            sys.exit()
        else:
            print(green("Resources retrieved succesfully."))
        run(["mkdir", "resources"])
        run(["tar", "-xvf", "vm_champs.tar", "-C", "resources"], stdout = DEVNULL, stderr = DEVNULL)
        run(["rm", "vm_champs.tar"])
    else:
        print(red("Could not continue the execution of the script."))
        sys.exit()

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

def find_project_dir(script_dir):
    '''Looks for a Corewar directory. The script's sibling and parent directories are searched,
    as well as the script directory itself.'''
    parent_dir = os.path.dirname(script_dir)
    print('script dir', script_dir)
    print('parent dir', parent_dir)
    dirs = [f.path for f in os.scandir(parent_dir) if f.is_dir()]
    dirs.append(script_dir)
    dirs.append(parent_dir)

    print("Checking if any of the following directories are a Corewar-directory:\n" + reduce(lambda x, y: x + '\n' + y, dirs))
    for dir in dirs:
        if is_corewar_root_dir(dir):
            return dir
    return None

def main():
    print(magenta("█▀▀ █▀█ █▀█ █▀▀ █░█░█ ▄▀█ █▀█   ▀█▀ █▀▀ █▀ ▀█▀ █▀\n█▄▄ █▄█ █▀▄ ██▄ ▀▄▀▄▀ █▀█ █▀▄   ░█░ ██▄ ▄█ ░█░ ▄█\n"))

    script_dir = os.path.dirname(os.path.realpath(__file__))

    if "resources" not in os.listdir(script_dir):
        retrieve_resources()
    resources_dir = script_dir + "/resources"
            
    if len(sys.argv) == 2:
        project_dir = sys.argv[1]
    else:
        project_dir = find_project_dir(script_dir)
        if project_dir is None:
            print(red("Error: Couldn't locate Corewar directory"))
            return

    print(green("Corewar directory found:"), project_dir)
    check_basic_stuff(project_dir)
    check_assembler(resources_dir, project_dir)
    check_virtual_machine()

if __name__ == '__main__':
    main()
