from contextlib import contextmanager
import argparse
import locale
import multiprocessing
import os
import sys
import traceback
from typing import Any, IO, List

from docutils.utils import SystemMessage

import sphinx.locale
from sphinx import __display_version__, package_dir
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx.locale import __
from docutils.parsers.rst.directives import _directives
from docutils.parsers.rst.roles import _roles
from sphinx.util import Tee, format_exception_cut_frames, save_traceback
from sphinx.util.console import nocolor, color_terminal, terminal_safe  # type: ignore
from sphinx.util.docutils import docutils_namespace, patch_docutils, docutils


@contextmanager
def yield_sphinx_app() -> Sphinx:
    """Sphinx build "main" command-line entry."""

    confdir = None
    confoverrides = {}
    # not necessarily needed
    sourcedir = (
        "/Users/cjs14/GitHub/sphinx/test_path/source"
    )  # path to documentation source files
    doctreedir = (
        "/Users/cjs14/GitHub/sphinx/test_path"
    )  # path for the cached environment and doctree
    outputdir = (
        "/Users/cjs14/GitHub/sphinx/test_path"
    )  # NOTE: outdir must exist otherwise it will be built
    builder = "html"

    status = sys.stdout
    warning = sys.stderr
    error = sys.stderr

    app = None
    try:
        with patch_docutils(confdir), docutils_namespace():
            app = Sphinx(
                sourcedir,
                confdir,
                outputdir,
                doctreedir,
                builder,
                confoverrides=confoverrides
                # optional
                #  args.builder, status,
                #  warning, args.freshenv, args.warningiserror,
                #  args.tags, args.verbosity, args.jobs, args.keep_going
            )
            # app.build(args.force_all, filenames)
            yield app, _directives, _roles
    except (Exception, KeyboardInterrupt) as exc:
        # handle_exception(app, args, exc, error)
        raise exc


from inspect import getdoc, getmro


def get_role_doc(role):
    return {"doc": getdoc(role)}


def get_directive_doc(direct):
    return {
        "doc": getdoc(direct),
        "required_arguments": direct.required_arguments,
        "optional_arguments": direct.optional_arguments,
        "has_content": direct.has_content,
        "options": {k: str(v.__name__) for k, v in direct.option_spec.items()}
        if direct.option_spec
        else "",
    }


import yaml

with yield_sphinx_app() as (app, directives, roles):
    print(
        yaml.safe_dump(
            {f"{name}": get_role_doc(r) for name, r in roles.items()},
            default_flow_style=False,
        )
    )
    print()
    print(
        yaml.safe_dump(
            {f"{name}": get_directive_doc(d) for name, d in directives.items()},
            default_flow_style=False,
        )
    )

