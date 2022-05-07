# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs on the [Issues Page](https://github.com/eswan18/premark/issues).

If you are reporting a bug, please include:

* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

### Write Documentation

Premark can always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is via the [Issues Page](https://github.com/eswan18/premark/issues).

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up Premark for local development.

1. Fork the [Premark repo](https://github.com/eswan18/premark) on GitHub.

2. Clone your fork locally:
    ```bash
    $ git clone https://github.com/your_name_here/premark.git
    ```

3. Install your local copy into a venv.
You'll Python 3.9 or above for this step.
Once you've `cd`ed into the base folder of the repository, follow these steps to get a venv set up for development on Premark:
    ```bash
    $ python3 -m venv .venv

    # Necessary for editable installs of a pyproject.toml codebase.
    $ pip install --upgrade pip

    $ . .venv/bin/activate

    $ pip install -e ".[dev]"
    ```

4. Create a branch for local development:
    ```bash
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
    Now you can make your changes locally.

5. Make your changes (update code, add tests, change docs, etc.).

6. When you're done making changes, check that your changes pass flake8, mypy, and the tests, including testing all supported Python versions with via tox:
    ```bash
    $ flake8 premark tests
    $ mypy premark
    $ pytest
    $ tox
    ```

7. Commit your changes and push your branch to GitHub:
    ```bash
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

8. Submit a pull request (to the develop branch of the original Premark repo) through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The PR should include new or updated tess for any functionality that has been changed.
2. New functions and classes should have descriptive docstrings adhering to the style of the rest of the package.
3. The CHANGELOG.md file should be updated with an account of your changes.
4. The code should work for Python versions 3.9 and above. Check and make sure that the tests pass for all supported Python versions.


## Releasing a New Version

The GitHub Actions pipeline is set up such that any Git tag starting with "v" will be built and published as a new version.
Ideally, merge changes into `main` and tag that commit (`git tag -a v1.2.3`), then push to GitHub including tags (`git push origin main --tags`).
