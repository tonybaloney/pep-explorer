#encoding: utf-8
'''
This file requires Python 3
'''
import pathlib
import json
import os
import re

_ver = re.compile(r'^\d+(\.\d+)*')
_here = pathlib.Path(__file__).parent


def _versionlike(s: str) -> tuple[tuple[int, ...], str]:
    m = _ver.match(s)
    if m is not None:
        parts = tuple(int(p) for p in m[0].split('.'))
        return parts, s
    else:
        return 999, s


def main():
    peps = []
    pep_directory = _here.joinpath('peps', 'peps')
    for item in pep_directory.iterdir():
        if item.suffix in ['.txt', '.rst'] and item.name.startswith('pep-'):
            peps.append(_pep_info(item))
    peps.sort(key=lambda p: p['PEP'])

    possible_statuses = sorted({p['Status'] for p in peps})
    possible_python_versions = sorted(
        {p['Python-Version'] for p in peps if 'Python-Version' in p},
        key=_versionlike,
    )
    possible_types = sorted({p['Type'] for p in peps})

    out = {
        'possible_statuses': possible_statuses,
        'possible_python_versions': possible_python_versions,
        'possible_types': possible_types,
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
    if 'Python-Version' in header:
        header['Python-Version'] = _fix_python_version(header['Python-Version'])
    header['PEP'] = int(header['PEP'])  # Better sorting
    return header


def _fix_python_version(version: str) -> str:
    '''
    Some inconsistency in the way target versions are done
    '''
    version = version.replace(' / ', ', ')
    version = version.replace(' and ', ', ')
    version = version.replace(' or ', ', ')
    version = version.replace(' and/or ', ', ')
    version = version.replace('3000', '3.0')
    return version

if __name__ == '__main__':
    main()
