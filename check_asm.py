import os
import sys
import re
from tempfile import NamedTemporaryFile
from typing import final
from library import *
from subprocess import CompletedProcess, run, PIPE

class AsmResult:
    def __init__(self, asm: str, f: str):
        self.result: CompletedProcess = run([asm, f], stdout = PIPE, stderr = PIPE, universal_newlines = True)
        self.outfile = None
        if self.result.returncode == 0:
            self.outfile = re.findall(r'/[a-zA-Z0-9\.\/\-\_]*', self.result.stdout)[0]

def compare(project_result: AsmResult, official_result: AsmResult) -> bool:
    is_success = True

    if project_result.result.returncode != official_result.result.returncode:
        print(orange("Warning:"),
              "Return code mismatch. Project returned {}, offical assembler returned {}."
              .format(project_result.result.returncode, official_result.result.returncode))
        is_success = False

    if project_result.outfile is None and official_result.outfile is not None:
        print(red("Error:"), "Your assembler did not produce a .cor file when the official one did.")
        is_success = False

    if project_result.outfile is not None and official_result.outfile is None:
        print(red("Error:"), "Your assembler produced a .cor file when the official one did not.")
        is_success = False

    return is_success


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

    for filename in os.listdir(resources_dir + "/champs"):
        if not filename.endswith(".s"):
            continue
        filepath = resources_dir + '/champs/' + filename
        with NamedTemporaryFile() as temp_a, NamedTemporaryFile() as temp_b:
            project_result = AsmResult(project_asm, filepath)
            official_result = AsmResult(official_asm, filepath)
            print("Testing with {:20s} -> ".format(filename), end = '')
            is_success = compare(project_result, official_result)
            if is_success:
                print(green("Success."))
            # diff_result = run(["diff", "--report-identical-files", str(temp_a.name), str(temp_b.name)], stdout = PIPE)
            # print(diff_result.stdout)
