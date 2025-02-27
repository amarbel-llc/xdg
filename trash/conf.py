import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'Trash Specification'
release = '1.0'

extensions = []
templates_path = ['_templates']
pygments_style = 'friendly'
html_theme = 'fdo-doc'
html_theme_path = [os.path.abspath(os.path.join('..', 'doc-builder', 'sphinx-themes'))]
html_theme_options = {}
