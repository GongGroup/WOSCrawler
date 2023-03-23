import subprocess
from pathlib import Path

from AICatalysis.common.constant import ChemInfo
from AICatalysis.database.reaxys import Reaxys


class Gaussian(object):
    pass


class GJFFile(object):
    def __init__(self, task="opt", method="b3lyp/6-31g(d,p)"):
        self.task = task
        self.method = method

    def read(self):
        pass

    def write(self, smiles: str, file='input.gjf'):
        process = subprocess.Popen(f"obabel -:{smiles} --gen3d -ogjf", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        content = process.stdout.read().decode(encoding='utf-8')
        lines = content.splitlines()
        chk_path = Path("").absolute() / Path(f"{file.removesuffix('.gjf')}.chk")
        lines[0] = f"%chk={chk_path}"
        lines[1] = f"#{self.task} {self.method}"
        lines[3] = "AutoGenerated"
        with open(file, "w") as f:
            f.write("\n".join(lines))


class OUTFile(object):
    def __init__(self, name="result.out"):
        self.name = name
        self.input_atoms = None

    def read(self):
        with open(self.name, "r") as f:
            self._strings = f.readlines()

        lns, lne = None, None
        for index, line in enumerate(self._strings):
            if line.startswith(" Symbolic Z-matrix"):
                lns = index
            elif line.startswith(" GradGrad"):
                lne = index
            if lns is not None and lne is not None:
                break

        _format = lambda x: [str(x[0]), float(x[1]), float(x[2]), float(x[3])]
        atom_lines = [l.split() for l in self._strings[lns + 2:lne - 2]]
        self.input_atoms = list(map(_format, atom_lines))
        
        pass
        return self


if __name__ == '__main__':
    # mapping = Reaxys.get_reaction_mapping()
    # catalysts = [name for name in list(mapping[0].keys()) if ChemInfo[name].get("smiles", None) is not None]
    # catalysts_smiles = [ChemInfo[name]['smiles'] for name in catalysts]
    # gjf = GJFFile()
    # for item, name in zip(catalysts_smiles, catalysts):
    #     print(f"{name}.gjf has been written")
    #     gjf.write(smiles=item, file=f"{name}.gjf")
    # print()
    out = OUTFile("../database/chemical-gjf/Ac2O.out")
    out.read()
    pass
