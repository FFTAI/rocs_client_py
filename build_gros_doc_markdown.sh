#!/bin/bash


sphinx-apidoc -o Sphinx-docs ./src sphinx-apidoc --full -A 'Matteo Ferla'; cd Sphinx-docs;

cp ../markdown_conf.py ./conf.py

make markdown

