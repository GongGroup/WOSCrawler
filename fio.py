import json
from pathlib import Path


def temp(file: Path):
    """
    Add "_" in the prefix of file, e.g., chemical.json -> _chemical.json

    Args:
        file: file path

    Returns:
        temp: new file path
    """
    return file.parent / f"_{file.name}"


class JsonIO(object):

    @staticmethod
    def read(file, encoding='utf-8'):
        """
        Json file read func

        Args:
            file: json file
            encoding: file encoding method

        Returns:
            data: python object load from json file
        """
        with open(file, 'r', encoding=encoding) as f:
            data = json.load(f)
        return data

    @staticmethod
    def write(obj, file, indent=2, encoding='utf-8'):
        """
        Json file write func

        Args:
            obj: python object you want to write in json
            file: json file
            indent: indent depth, default: 2
            encoding: file encoding method, default: utf-8

        """
        with open(file, "w", encoding=encoding) as f:
            json.dump(obj, f, indent=indent)


if __name__ == '__main__':
    path = Path("reaxys_json.json")
    temp_path = temp(path)
    print()
