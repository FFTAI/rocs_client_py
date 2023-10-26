import os
import sys

project = 'Fourier-GROS'
copyright = '2023, Fourier Software Department'
author = 'Fourier Software Department'
release = '1.0'

sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    "sphinx_markdown_builder"
]

exclude_patterns = []

language = 'zh_CN'
