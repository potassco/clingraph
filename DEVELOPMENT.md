# Development

To improve code quality, we use [nox] to run linters, type checkers, unit
tests, and more. We recommend installing nox using [pipx] to have it available
globally.

```bash
# install
python -m pip install pipx
python -m pipx install nox

# run all sessions
nox

# list all sessions
nox -l

# run individual session
nox -s session_name

# run individual session (reuse install)
nox -Rs session_name
```

Note that the nox sessions create [editable] installs. In case there are
issues, try recreating environments by dropping the `-R` option. If your
project is incompatible with editable installs, adjust the `noxfile.py` to
disable them.

We also provide a [pre-commit][pre] config to autoformat code upon commits. It
can be set up using the following commands:

```bash
python -m pipx install pre-commit
pre-commit install
```

## Documentation

Make sure the documentation dependencies for the project are properly installed
with

```bash
pip install .[doc]
```

To run the documentation locally use the following command and click the
provided link to open it in the browser.

```bash
mkdocs serve
```

[editable]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
[nox]: https://nox.thea.codes/en/stable/index.html
[pipx]: https://pypa.github.io/pipx/
[pre]: https://pre-commit.com/
