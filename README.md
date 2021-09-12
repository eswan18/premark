# Premark

[![CI Status](https://github.com/eswan18/premark/actions/workflows/ci.yaml/badge.svg)](https://github.com/eswan18/premark/actions/workflows/ci.yaml)
[![Docs Status](https://readthedocs.org/projects/premark/badge/?version=latest)](https://premark.readthedocs.io/en/latest/?badge=latest)

Premark generates single-file HTML presentations from one or many markdown files, using [Remark.js](https://github.com/gnab/remark).
Based on [Remarker](https://github.com/tylerdave/remarker) by @tylerdave.

License: MIT

Documentation: [Read The Docs](https://premark.readthedocs.io/en/latest/)

## Notable Features

- The output is always a *single* HTML file. This means you can open it in your browser without spinning up a web server.
  - In contrast, with vanilla Remark, if your main HTML file needs to load any other files then it can't be opened locally without a web server.

- Your slides can be stored in multiple markdown files and Premark will automatically "stitch" them together into a single presentation, even creating title slides for each section if you want.

## Usage Example

Generate `presentation.html` from Markdown in `slides.md`:

```bash
premark -o presentation.html slides.md
```
