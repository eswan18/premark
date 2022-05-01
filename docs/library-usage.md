# Using as a Python Library

Premark exposes a `Presentation` class that can be used to create presentations from within Python.

```python
from premark import Presentation

my_markdown = '''
class: center, middle
# My Presentation

...
'''

# Create a presentation object from some markdown
p = Presentation(markdown=my_markdown)

# Render the presentation as HTML
html = p.to_html()
# You probably want to save the HTML to a file
with open('prez.html', 'w') as f:
    f.write(html)
```

## Creating Presentations

There are three ways of creating a new presentation:
1. Passing a markdown source file.
2. Passing a directory of markdown source files.
3. Passing literal markdown text.

### 1. From a single markdown file

```
p = Presentation('path/to/markdown.md')
```
This is the simplest approach.
The argument may be a string, a `pathlib.Path`, or a file-like object (one supporting a `read()` method).

### 2. From a directory of markdown files

```
p = Presentation('path/to/markdown_directory', config_file='conf.yaml')
```

When passing a directory as the source, a configuration file (in YAML) is required.
In this file you must specify the order in which to combine your markdown files.
For example:
```yaml
sections:
- intro.md
- section_1.md
- section_2.md
- conclusion.md
```

All of these files must exist inside the source directory.

A more verbose syntax in the `sections` configuration can unlock more Premark features.
By specifying sections using both `file` and `title`, Premark will automatically include a title slide before each new section.

```yaml
sections:
- file: intro.md
  title: Introduction
- file: section_1.md
  title: The Interface of My Project
- file: section_2.md
  title: The Implementation of My Project
- file: conclusion.md
  title: Wrapping Up
```

### 3. From literal markdown

Premark can accommodate markdown already stored in a string.
Pass it using the `markdown` keyword argument.

```python
md = '# Welcome\n---## Agenda\n1. Content'
p = Presentation(markdown=md)
```



## Customizing Presentations

As seen above, literal markdown or a file source is required when creating a new presentation.
Other parameters are optional, but can be very useful for customizing your rendered slides.

Parameters:
- `html_template` (str, Path, or file-like) -- A file containing a custom HTML Jinja template into which the title, markdown, stylesheet, and remark arguments should be inserted, overriding the default one. (All those fields are expected to be present in the template, e.g. `{{ title }}`)
- `stylesheet` (str, Path, or file-like) -- A file containing the CSS styles to insert into the presentation, overriding the default one.
- `title` (str) -- The title of the rendered presentation. Has no impact on the slides themslves but is inserted in the HTML title tag.
- `remark_args` (dict) -- the arguments to pass to `remark.create`, overriding the defaults.

For full documentation of the available arguments when creating `Presentation`s, see the [API docs](api.html#premark.presentation.Presentation).


## Config Files

While -- except for section ordering and titling -- all presentation customization can be done without a separate config file, using config files is well worth it when working on presentations that you intend to rebuild repeatedly.
In such cases, leaving a `config.yaml` in the directory allows you to version control your Premark configuration.

If the `config_file` argument is passed to `Presentation`, that file is read and its values used as configuration *unless* the same value was also passed as an argument.
(Explicit arguments always take priority.)
Additionally, the ordering of multiple presentation "sections" can *only* be specified via a config file.

Your config file might look like this:
```yaml
sections:
- intro.md
- agenda.md
- main_content.md
- closing.md
title: The Best Slideshow
stylesheet: assets/styles.css
```

Along with (or instead of) `stylesheet` and `title`, `html_template` is also an accepted argument.


## Laying Out Your Project

In most cases, if you're using Premark, you have one or several markdown files containing slides and those live in a project folder of some sort -- and that project is in version control.
A good layout in such cases is to keep your config file in the base of the repo and name it `premark.yaml`, and your slides in an `premark_slides` folder.
If you have custom HTML or CSS files, put them in an `premark_assets/` folder.

```text
myproject
├── premark.yaml
├── premark_assets
├   ├── template.html
├   └── styles.css
└── premark_slides
    ├── agenda.md
    ├── closing.md
    ├── exercises.md
    ├── intro.md
    └── main_content.md
```

And the contents of `premark.yaml` might look like this:

```yaml
sections:
- file: intro.md
- file: agenda.md
- file: main_content.md
- file: closing.md
- file: exercises.md
stylesheet: premark_assets/styles.css
html_template: premark_assets/template.html
title: A Wild Ride
```

With this format, you can store Premark presentations in the same folder as related projects.
This may not be necessary in most cases, but this kind of organization is very handy occasionally.

## Exporting Presentations (i.e. *Rendering*)

There's only one format for exporting presentations: HTML.
The `.to_html` method performs the conversion for you:

```
p = Presentation(...)
html = p.to_html()
```

That's it!

[API docs](api.html#premark.presentation.Presentation.to_html)
