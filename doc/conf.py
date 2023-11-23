import os
import sys

project = 'Fourier-RoCS'
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
    'sphinx_wagtail_theme',
    'sphinx_markdown_builder'
]

html_theme = 'sphinx_wagtail_theme'
exclude_patterns = []

language = 'zh_CN'
