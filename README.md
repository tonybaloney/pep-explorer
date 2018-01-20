# pep-explorer.github.io
An easy to use online explorer for Python Enhancement Proposals


## Updating the index

The pep/ directory is a git submodule for the actual PEP repository on Github

```bash
cd peps
git pull
cd ..
python3 genindex.py
```
