#!/bin/bash

# Run Unimport.
unimport ./ --ignore-init --gitignore -r

# Run Isort.
isort ./

# Run our lint script.
python ./.github/workflows/scripts/lint.py

# Run Flynt.
flynt ./ -tc

# Run Black.
black ./

echo
echo
echo "Linting finished!"
