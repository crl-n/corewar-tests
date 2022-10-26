import os
import sys
import re
from tempfile import NamedTemporaryFile
from library import *
from subprocess import CompletedProcess, run, PIPE

class AsmResult:
    def __init__(self, asm: str, f: str):
        self.result: CompletedProcess = run([asm, f], stdout = PIPE, stderr = PIPE, universal_newlines = True)
        self.outfile = None
        if self.result.returncode == 0:
            self.outfile = re.findall(r'/[a-zA-Z0-9\.\/\-\_]*', self.result.stdout)[0]

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

    for f in [resources_dir + '/champs/' + f for f in os.listdir(resources_dir + "/champs") if f.endswith(".s")]:
        print("Comparing " + f)
        with NamedTemporaryFile() as temp_a, NamedTemporaryFile() as temp_b:
            project_result = AsmResult(project_asm, f)
            official_result = AsmResult(official_asm, f)
            print(project_result.outfile)
            print(official_result.outfile)
            # diff_result = run(["diff", "--report-identical-files", str(temp_a.name), str(temp_b.name)], stdout = PIPE)
            # print(diff_result.stdout)
