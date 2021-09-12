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
html = p.to_html(title='My Presentation')
# You probably want to save the HTML to a file
with open('prez.html', 'w') as f:
    f.write(html)
```

### Creating Presentations

There are three ways of creating a new `Presentation` object:

#### Through the standard initializer

```
p = Presentation(markdown)
```
This is the simplest approach.
The markdown provided can be either a string of raw markdown or a `pathlib.Path` object pointing to a file containing the markdown.
You may optionally provide `html_template` and `stylesheet` arguments for custom HTML and CSS respectively.

```
p = Presentation(markdown, html_template, stylesheet)
```

The final presentation will include the passed-in markdown with no modifications.

[API docs](api.html#premark.presentation.Presentation)

#### From a directory of markdown files

```
p = Presentation.from_directory(directory)
```

This is how Premark supports "stitching" multiple individual presentations together as sections of a larger presentation.
The directory must contain a metadata file defining the order in which the sections should be combined, along with whether each should have a title automatically added.
For example, a slide directory might like this :

```text
slide_sections
├── agenda.md
├── closing.md
├── exercises.md
├── intro.md
├── main_content.md
└── sections.yaml
```

And the contents of `sections.yaml` like this:

```yaml
# sections.yaml
sections:
- file: intro.md
- file: agenda.md
- file: main_content.md
- file: closing.md
- file: exercises.md
```

Then `Presentation.from_directory('./slide_sections')` will build a combined presentation with the contents of intro.md, agenda.md, main_content.md, closing.md, and exercises.md (in that order).


By default, the metadata file is expected to be named `sections.yaml`, but this can be customized by passing a different string as the `metafile` argument of `from_directory`:

```python
# If the metafile is actually at slide_sections/stich_order.yaml
Presentation.from_directory('./slide_sections', metafile='stitch_order.yaml')
```

Note that the metadata file must always be in the same directory as the individual slide files, and must be in yaml format.

For any section that has an additional "title" key in the metadata file, Premark will automatically add a section title slide along with a section number.
You can mix titled and untitled sections in the same metadata file.

```yaml
# sections.yaml
sections:
- file: intro.md
- file: agenda.md
  title: Agenda
- file: main_content.md
  title: "Today's Main Content"
- file: closing.md
  title: Wrap-up
- file: exercises.md
```

Invoked this way, Premark will add lead slides to the agenda, main_content, and closing sections.
Those slides have a section number and title, and will have the `center` and `middle` classes applied (so the text is centered on the slide).
```markdown
class: center, middle

## #3
# Wrap-up
```

Sections without an automatic title slide aren't counted by Remark -- so here, *Agenda* is #1, *Today's Main Content* is #2, and *Wrap-up* is #3.
But if the agenda section didn't have a title key in the metadata file, then *Today's Main Content* would be #1 and *Wrap-up* would be #2.

[API docs](api.html#premark.presentation.Presentation.from_directory)

#### From a collection of other Presentation objects

If you prefer to provide several `Presentation` objects yourself and have Premark join them together, simply pass an iterable of them to `Presentation.from_presentations`:

```python
prez_1 = Presentation(...)
prez_2 = Presentation(...)
prez_3 = Presentation(...)

final_prez = Presentation.from_presentations([prez_1, prez_2, prez_3])
```

[API docs](api.html#premark.presentation.Presentation.from_presentations)


### Exporting Presentations

There's only one format for exporting presentations: HTML.
The `.to_html` method performs the conversion for you:

```
p = Presentation(...)
html = p.to_html()
```

You may optionally provide a `title` argument to `to_html`, which will become the contents of the `<title>` tag in the result.
(It has no effect on the contents of the slides themselves.)

```
html = p.to_html(title='Lecture 1')
```

If no title is provided, the default is "Premark Presentation".

[API docs](api.html#premark.presentation.Presentation.to_html)
