# Using from the Command Line

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

### Breaking Markdown into Sections

Premark can combine multiple markdown files containing slide definitions into a single final presentation.
Simply put all the markdown files in a single folder (say, `slide_sections`) along with a `sections.yaml` file like the below:

```yaml
sections:
- file: intro.md
- file: agenda.md
- file: closing.md
```

Then, when invoked with the below command, Premark will search that `slide_sections` directory for `intro.md`, `agenda.md`, and `closing.md`, merging them and producing a single presentation from the result.

```bash
premark -o presentation.html slide_sections
```

Premark can even add title slides to each section.
Simply provide a `title` key in the section metadata file:
```yaml
sections:
- file: intro.md
- file: agenda.md
  title: Agenda
- file: closing.md
  title: Final Thoughts
```

Sections without a `title` key will not have a title slide added and aren't counted when numbering the sections.

### Custom CSS or HTML

Premark allows you to specify your own CSS or HTML template to be used in the final presentation, through the `--css-file` and `--html-template` options.

```bash
premark -o presentation.html --css-file styles.css slides.md
```
```bash
premark -o presentation.html --html-template template.html slides.md
```
