import os
from subprocess import run, PIPE
from library import *

def check_basic_stuff(dir):
    '''Checks Makefile, author-file and norm.'''
    print(magenta("\nBasic Stuff"))
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

