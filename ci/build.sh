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
python3 -m compileall -q main.py pricing.py
echo "STAGE quality"
python3 -m flake8 main.py pricing.py test_pricing.py
echo "STAGE tests"
python3 -m unittest -v
echo "STAGE package"
python3 -m zipfile -c "/out/workshop-$BUILD_NUMBER.zip" main.py pricing.py
python3 main.py
