#encoding: utf-8
'''
This file requires Python 3
'''
import pathlib
import json


def main():
    peps = []
    pep_directory = pathlib.Path('peps/')
    for item in pep_directory.iterdir():
        if item.suffix == '.txt' and item.name.startswith('pep-'):
            peps.append(_pep_info(item))
    possible_statuses = set([p['Status'] for p in peps])
    possible_python_versions = set([p['Python-Version'] for p in peps if 'Python-Version' in p])
    out = {
        'possible_statuses': list(possible_statuses),
        'possible_python_versions': list(possible_python_versions),
        'peps': peps
    }

    with open('index.json', 'w+') as index_json:
        index_json.write(json.dumps(out,
                         indent=4, separators=(',', ': ')))


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
    header['URL'] = 'https://python.org/dev/peps/{0}/'.format(pep_path.stem)
    return header


if __name__ == '__main__':
    main()