===============================
Remarker
===============================

.. image:: https://img.shields.io/travis/tylerdave/remarker.svg
        :target: https://travis-ci.org/tylerdave/remarker

.. image:: https://img.shields.io/pypi/v/remarker.svg
        :target: https://pypi.python.org/pypi/remarker

.. image:: https://coveralls.io/repos/github/tylerdave/remarker/badge.svg?branch=master
        :target: https://coveralls.io/github/tylerdave/remarker?branch=master

A command line tool for generating `Remark.js <https://github.com/gnab/remark>`_ presentations from markdown files.

License: MIT

Documentation: https://remarker.readthedocs.org.

Usage
-----

``remarker --help``

.. code-block:: none

  Usage: remarker [OPTIONS] SLIDES_MARKDOWN_FILE
  
    Generate a Remark.js HTML presentation from input Markdown and optional
    custom CSS.
  
  Options:
    --version                   Show the version and exit.
    -v, --verbose               Output debugging info.
    -t, --title TEXT            HTML title of the presentation.
    -o, --output-file FILENAME  Write the output to a file instead of STDOUT.
    -c, --css-file PATH         Custom CSS to be included inline.
    --html-template PATH        Jinja2 template file for the presentation.
    --help                      Show this message and exit.


Usage Examples
--------------

Generate ``presentation.html`` from Markdown in ``slides.md``:

.. code-block:: shell

  remarker -o presentation.html slides.md

Generate ``presentation.html`` from Markdown in ``slides.md`` and CSS in
``style.css``:

.. code-block:: shell

  remarker -o presentation.html -c style.css slides.md
