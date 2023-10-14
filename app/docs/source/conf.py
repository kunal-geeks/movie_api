
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# conf.py

from unittest.mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = ['flask', 'flask_sqlalchemy', 'flask_mail', 'other_flask_modules', 'flask.typing']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# Include private and protected members in the documentation
autodoc_default_options = {
    'members': True,
    'private-members': True,
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
}

project = 'MOVIE_API'
copyright = '2023, Kunal Sharma'
author = 'Kunal Sharma'
release = 'v1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.httpdomain',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# Output directory for build files
html_output_dir = '../build/html'