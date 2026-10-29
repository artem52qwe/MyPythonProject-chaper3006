#!/bin/bash
set -eu
trap 'result=$?; python3 /source/ci/notify.py "$result"' EXIT
echo "STAGE checkout: read-only mirror of GitHub repository"
git config --global --add safe.directory /source
git config --global --add safe.directory /source/.git
git clone /source "workshop-$BUILD_NUMBER"
cd "workshop-$BUILD_NUMBER"
if [ "$BUILD_NUMBER" = 1 ]; then git checkout ci-before; else git checkout ci-after; fi
git log -1 --format='%H %s'
echo "STAGE dependencies: Python and flake8 installed in immutable image"
python3 --version
python3 -m flake8 --version
echo "STAGE syntax"
python3 -m compileall -q .
echo "STAGE quality"
python3 -m flake8 ./*.py
echo "STAGE tests"
python3 -m unittest -v
echo "STAGE package"
python3 -m zipfile -c "/out/workshop-$BUILD_NUMBER.zip" ./*.py README.md requirements.txt
python3 -m zipfile -e "/out/workshop-$BUILD_NUMBER.zip" package-check
(cd package-check && python3 main.py && python3 -m unittest -v)
python3 main.py
