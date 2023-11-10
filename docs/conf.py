# Author: Dominik Harmim <harmim6@gmail.com>

"""Sphinx configuration."""

import sys
from datetime import datetime
from os.path import abspath, exists
from os.path import join as join_path
from shutil import rmtree

from sphinx.application import Sphinx
from sphinx.ext import apidoc


def __run_apidoc(app: Sphinx) -> None:
    """
    Generate doc stubs using sphinx-apidoc.

    :param Sphinx app: Sphinx application API
    """
    module_dir = join_path(app.srcdir, "../src")
    output_dir = join_path(app.srcdir, "_apidoc")

    # Ensure that any stale apidoc files are cleaned up first.
    if exists(output_dir):
        rmtree(output_dir)

    apidoc.main([
        "--separate",
        "--module-first",
        "--doc-project=API Reference",
        "-o",
        output_dir,
        module_dir,
    ])


def setup(app: Sphinx) -> None:
    """
    Register the sphinx-apidoc hook.

    :param Sphinx app: Sphinx application API
    """
    app.connect("builder-inited", __run_apidoc)


# For correct paths.
sys.path.insert(0, abspath(".."))


### Sphinx configuration below.

project = "Kiwi.com - Itineraries Sorting"
copyright = "Copyright (c) {}, Dominik Harmim <harmim6@gmail.com>".format(
    datetime.now().year,
)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

source_suffix = ".rst"
master_doc = "index"

autoclass_content = "class"
autodoc_member_order = "bysource"
default_role = "py:obj"

html_theme = "haiku"
