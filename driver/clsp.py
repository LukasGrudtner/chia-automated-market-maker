from typing import List
from pathlib import Path

from chia.types.blockchain_format.program import Program

from clvm_tools.clvmc import compile_clvm
from clvm_tools.binutils import disassemble, assemble

from cdv.cmds.util import parse_program, append_include
from driver import utils


def build(files: List[str], include: List[str]) -> None:
    project_path = Path.cwd()
    clvm_files = []
    for glob in files:
        for path in Path(project_path).rglob(glob):
            if path.is_dir():
                for clvm_path in Path(path).rglob("*.cl[vs][mp]"):
                    clvm_files.append(clvm_path)
            else:
                clvm_files.append(path)

    for filename in clvm_files:
        hex_file_name: str = filename.name + ".hex"
        full_hex_file_name = Path(filename.parent).joinpath(hex_file_name)
        # We only rebuild the file if the .hex is older
        if not (full_hex_file_name.exists() and full_hex_file_name.stat().st_mtime > filename.stat().st_mtime):
            outfile = str(filename) + ".hex"
            try:
                print("Beginning compilation of " + filename.name + "...")
                compile_clvm(str(filename), outfile, search_paths=append_include(include))
                print("...Compilation finished")
            except Exception as e:
                print("Couldn't build " + filename.name + ": " + str(e))


def curry(program: str, args: List[str], include: List[str], treehash: bool = False, dump: bool = False) -> str:
    prog: Program = parse_program(program, include)
    curry_args: List[Program] = [assemble(arg) for arg in args]

    prog_final: Program = prog.curry(*curry_args)
    if treehash:
        return str(prog_final.get_tree_hash())
    elif dump:
        return str(prog_final)
    else:
        return disassemble(prog_final)


def solution(args: List[object]) -> str:
    return str(Program.to(args))
