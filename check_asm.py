import os
import sys
import time
from tempfile import NamedTemporaryFile
from library import *
from subprocess import run, PIPE

def check_assembler(resources_dir, project_dir):
    print(magenta("\nAssembler tests"))
    project_asm = project_dir + "/asm"
    official_asm = resources_dir + "/asm"

    if not os.path.exists(project_asm):
        print(red("Error: Couldn't find your assembler."))
        sys.exit()
    if not os.path.exists(official_asm):
        print(red("Error: Couldn't find the official assembler."))
        sys.exit()

    f = ""
    for f in [resources_dir + '/champs/' + f for f in os.listdir(resources_dir + "/champs") if f.endswith(".s")]:
        print("Comparing " + f, end = "\r")
        with NamedTemporaryFile() as temp_a, NamedTemporaryFile() as temp_b:
            result_a = run([project_asm, f], stdout = PIPE, stderr = PIPE)
            result_b = run([official_asm, f], stdout = PIPE, stderr = PIPE)
            temp_a.write(result_a.stdout)
            temp_b.write(result_b.stdout)
            # temp_a.seek(0)
            # temp_b.seek(0)
            # print(temp_a.name, temp_b.name)
            diff_result = run(["diff", "--report-identical-files", str(temp_a.name), str(temp_b.name)], stdout = PIPE)
            time.sleep(0.03)
            print("\033[2K", end = "")
    print("Comparing " + f)

