import sys
import os

from datetime import datetime

import alabaster

sys.path.insert(0, os.path.abspath(".."))


project = "candv"
version = "1.5"
release = "1.5.0"
year = datetime.now().year
copyright = f"{year}, Oleksandr Oblovatnyi"

pygments_style = "sphinx"

html_theme = "alabaster"
html_sidebars = {
  "**": [
    "about.html",
    "searchbox.html",
    "navigation.html",
  ]
}
html_theme_options = {
  'description': "A Python library for creating complex enum-like constants",
  'show_related': False,
  'show_relbars': True,
  'github_user': "oblalex",
  'github_repo': "candv",
  'github_banner': "true",
  'github_button': "true",
  'github_count': "true",
  'github_type': "star",
}
html_theme_path = [
  alabaster.get_path(),
]

extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.intersphinx",
  "sphinx.ext.todo",
  "sphinx.ext.viewcode",
]

htmlhelp_basename = "candvdoc"
templates_path = ["_templates"]
exclude_patterns = ["_build"]
todo_include_todos = True
source_suffix = ".rst"
master_doc = "index"

autodoc_default_options = {
  'member-order': 'bysource',
}

intersphinx_mapping = {
  "https://docs.python.org/3": None,
}
