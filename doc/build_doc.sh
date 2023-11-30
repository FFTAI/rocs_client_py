#!/bin/sh

rm -rf source
rm -rf build
rm -rf

mkdir -p build/
mkdir -p source/_static

cp ico.jpg ./source/_static/
cp conf.py ./source/
cp index.rst ./source/


sphinx-apidoc -o source ../
make dirhtml
make markdown