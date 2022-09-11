#!/usr/bin/env python3

import os
from subprocess import run, PIPE, DEVNULL
from functools import reduce

def magenta(str):
    return "\033[35m" + str + "\033[0m"

def red(str):
    return "\033[31m" + str + "\033[0m"

def green(str):
    return "\033[32m" + str + "\033[0m"

def check_basic_stuff(dir):
    '''Checks Makefile, author-file and norm.'''
    files = [f for f in os.listdir(dir)]

    if "Makefile" not in files:
        print(red("No Makefile found"))
    else:
        print(green("Makefile found"))

    if "author" not in files:
        print(red("No author file found"))
    else:
        author_contents = run(["cat", dir + "/author"], stdout = PIPE)
        print(green("Author file found:"), str(author_contents.stdout, 'utf-8').replace('\n', '\\n'))

    norm_result = run(["norminette"], stdout = PIPE)
    if norm_result.returncode != 1:
        print(red("Norminette found norm errors!"))
    else:
        print(green("Norm OK"))

def check_assembler():
    pass

def check_virtual_machine():
    pass

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
    print(magenta("█▀▀ █▀█ █▀█ █▀▀ █░█░█ ▄▀█ █▀█   ▀█▀ █▀▀ █▀ ▀█▀ █▀\n█▄▄ █▄█ █▀▄ ██▄ ▀▄▀▄▀ █▀█ █▀▄   ░█░ ██▄ ▄█ ░█░ ▄█"))

    script_dir = os.path.dirname(os.path.realpath(__file__))

    if "resources" not in os.listdir(script_dir):
        if input(red("The official 42 Corewar resources could not be found.") + " Would you like to download them from intra.42.fr? (yes/no) ") in ['y', 'yes', 'Y' , 'Yes']:
            curl_result = run(['curl', '--remote-name', 'https://projects.intra.42.fr/uploads/document/document/1170/vm_champs.tar'], stdout = DEVNULL, stderr = DEVNULL)
            if curl_result.returncode != 0:
                print(red("Error: Could not download resources from intra.42.fr. Check you network connection."))
                return
            else:
                print(green("Resources retrieved."))
            run(["mkdir", "resources"])
            run(["tar", "-xvf", "vm_champs.tar", "-C", "resources"], stdout = DEVNULL, stderr = DEVNULL)
            run(["rm", "vm_champs.tar"])
        else:
            print(red("Could not continue the execution of the script."))
            return
            
    project_dir = find_project_dir(script_dir)
    if project_dir is None:
        print(red("Error: Couldn't locate Corewar directory"))
        return

    print(green("Corewar directory found:"), project_dir)
    check_basic_stuff(project_dir)
    check_assembler()
    check_virtual_machine()

if __name__ == '__main__':
    main()
