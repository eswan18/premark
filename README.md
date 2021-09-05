# Premark

[![CI Badge](https://github.com/eswan18/premark/actions/workflows/ci.yaml/badge.svg)](https://github.com/eswan18/premark/actions/workflows/ci.yaml)

A lightweight, command line preprocessor for creating [Remark.js](https://github.com/gnab/remark) presentations from markdown files.

License: MIT

Documentation: *TBD*

## Headline Features

* Even when using multiple input files (custom CSS and/or a markdown file separate from your HTML template), the output is always a single HTML file. This means you can open it in your browser without spinning up a web server. In contrast, with vanilla Remark, if your main HTML file needs to load any other files then it can't be opened locally without a web server.

* Supports "section stitching" -- you can store multiple sets of markdown slides in a single folder and Premark will stitch them together into a single slideshow. This can be very handy when your presentation becomes large enough that it's cumbersome to keep in a single file.

## Usage

```bash
premark --help
```

```
Usage: premark [OPTIONS] SLIDE_SOURCE

Generate a Remark.js HTML presentation from input Markdown and optional
custom CSS.

Options:
--version                    Show the version and exit.
-v, --verbose                Output debugging info.
-t, --title TEXT             HTML title of the presentation.
-o, --output-file FILENAME   Write the output to a file instead of STDOUT.
-m, --metafile TEXT          File definition for the order of section
                             stitching. Only needed if using a sections
                             folder.

-c, --css-file PATH          Custom CSS to be included inline.
--html-template PATH         Jinja2 template file for the presentation.
--help                       Show this message and exit.
```

## Usage Examples

Generate `presentation.html` from Markdown in `slides.md`:

```bash
premark -o presentation.html slides.md
```

Generate `presentation.html` from Markdown in `slides.md` and CSS in `style.css`:

```bash
premark -o presentation.html -c style.css slides.md
```

Generate ``presentation.html`` from a folder ``slide_sections`` containing multiple markdown files along with a ``sections.yaml`` file defining the order in which to collate them:

```bash
premark -o presentation.html slide_sections
```

