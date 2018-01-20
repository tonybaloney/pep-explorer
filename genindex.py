#encoding: utf-8
'''
This file requires Python 3
'''
import pathlib
from collections import OrderedDict
import json

def main():
    peps = OrderedDict()
    pep_directory = pathlib.Path('peps/')
    for item in pep_directory.iterdir():
        if item.suffix == '.txt' and item.name.startswith('pep-'):
            peps[item.name] = _pep_info(item)

    with open('index.json', 'w+') as index_json:
        index_json.write(json.dumps(peps))


def _pep_info(pep_path: pathlib.Path) -> dict:
    header = {}
    last_attribute = None
    with open(pep_path, 'r') as pep_file:
        while True:
            line = pep_file.readline()
            if line == '\n':
                break
            else:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    attribute = parts[0]
                    last_attribute = attribute
                    value = parts[1].strip()
                    header[attribute] = value
                else:
                    header[last_attribute] += ',' + parts[0].strip()
    return header


if __name__ == '__main__':
    main()