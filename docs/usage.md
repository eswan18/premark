# Usage

Commands are generally of the form:
```bash
premark [OPTIONS] SLIDE_SOURCE
```

The simple invocation below reads input from `slides.md`, parses it, and writes the resulting RevealJS slideshow to `presentation.yaml`.
```bash
premark -o presentation.html slides.md
```

`SLIDE_SOURCE` can be the name of a single markdown file (formatted as slides, as RevealJS expects) or the name of a folder with multiple such files inside along with a `sections.yaml` file.

Available options are below:

| Option                     | Description
|----------------------------|-----------------------------------------------|
|`--version`                 | Show the version and exit.                    |
|`-v, --verbose`             | Output debugging info.                        |
|`-t, --title TEXT`          |  HTML title of the presentation.              |
|`-o, --output-file FILENAME`|  Write the output to a file instead of STDOUT.|
|`-m, --metafile TEXT`       |  File definition for the order of section stitching. Only needed if using a sections folder.|
|`-c, --css-file PATH`       |  Custom CSS to be included inline.            |
|`--html-template PATH`      |  Jinja2 template file for the presentation.   |
|`--help`                    |  Show this message and exit.                  |

## Usage Examples

Generate `presentation.html` from Markdown in `slides.md` and CSS in `style.css`:

```bash
premark -o presentation.html -c style.css slides.md
```

Generate ``presentation.html`` from a folder ``slide_sections`` containing multiple markdown files along with a ``sections.yaml`` file defining the order in which to collate them:

```bash
premark -o presentation.html slide_sections
```

