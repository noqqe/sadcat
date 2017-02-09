#!/usr/bin/env bash

echo bump version
bumpversion minor VERSION

v=$(cat VERSION)

echo adding local file
git add VERSION

echo commit
git commit -a -m "Release: $v"

echo tagging..
git tag v${v}

echo pushing..
git push --tags origin master

echo release on pypi
python setup.py sdist upload -r pypi

echo install locally
pip install --upgrade .
