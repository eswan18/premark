# Premark

[![CI/CD Status](https://github.com/eswan18/premark/actions/workflows/cicd.yaml/badge.svg)](https://github.com/eswan18/premark/actions/workflows/cicd.yaml)
[![Docs Status](https://readthedocs.org/projects/premark/badge/?version=latest)](https://premark.readthedocs.io/en/latest/?badge=latest)
[![codecov Status](https://codecov.io/gh/eswan18/premark/branch/main/graph/badge.svg?token=PCS1RGIS5D)](https://codecov.io/gh/eswan18/premark)

Premark generates single-file HTML presentations from one or many markdown files, using [Remark.js](https://github.com/gnab/remark).
Based on [Remarker](https://github.com/tylerdave/remarker) by [@tylerdave](https://github.com/tylerdave).

License: MIT

Documentation: [Read The Docs](https://premark.readthedocs.io/en/latest/)

## Notable Features

- Create slides from simple Markdown. Use three dashes on their own line (`---`) to indicate the transition from one slide to another. All other markdown features work as expected.

- The output is always a *single* HTML file. This means you can open it in your browser without spinning up a web server.
  - In contrast, with vanilla Remark, if your main HTML file needs to load any other files then it can't be opened locally without a web server.

- Your slides can be stored in multiple markdown files and Premark will automatically "stitch" them together into a single presentation, even creating title slides for each section if you want.

## Usage Example

Generate `presentation.html` from Markdown in `slides.md`:

```bash
premark -o presentation.html slides.md
```

You can also pass in a custom CSS file to style your presentation.

```bash
premark -o presentation.html --stylesheet style.css slides.md
```

### Creating a Presentation from Multiple Sections

You may wish to build your presentation from multiple markdown files, each representing a "section" of the final slideshow.
Premark supports this through the use of a configuration file, where you can specify the order of your sections.

Say you have a folder `md_slides` containing individual sections `intro.md`, `section_1.md`, `section_2.md`, and `closing.md`.
You could create a config file like the following:

```yaml
# config.yaml
sections:
- intro.md
- section_1.md
- section_2.md
- closing.md
```
 
And then invoke Premark with
```bash
premark -c config.yaml -o slides.html md_slides
```

The resulting `slides.html` will contain all four sections.
