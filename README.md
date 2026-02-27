# Sparv – Språkbanken's Analysis Platform

Sparv is a text analysis tool run from the command line. The documentation can be found here:
<https://spraakbanken.gu.se/sparv>.

Check the [changelog](CHANGELOG.md) to see what's new!

Sparv is developed by [Språkbanken](https://spraakbanken.gu.se/). The source code is available under the [MIT
license](https://opensource.org/licenses/MIT).

If you have any questions, problems or suggestions please contact <sb-sparv@svenska.gu.se>.

## Prerequisites

* A Unix-like environment (e.g. Linux, OS X or [Windows Subsystem for
  Linux](https://docs.microsoft.com/en-us/windows/wsl/about)) *Note:* Most of Sparv's features should work in a Windows
  environment as well, but since we don't do any testing on Windows we cannot guarantee anything.
* [Python 3.11](https://python.org/) or newer.

## Installation

Sparv is available on [PyPI](https://pypi.org/project/sparv/) under the name `sparv`. Refer to the [Sparv user
manual](https://spraakbanken.gu.se/sparv/user-manual/installation-and-setup/) for detailed installation and setup
instructions.

## Development

To set up a development environment for Sparv, we recommend using [uv](https://docs.astral.sh/uv/) to create a
virtual environment and install the dependencies.

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it already.
2. While in the Sparv project directory, run:

   ```sh
   uv sync
   ```

   This will create a virtual environment in the `.venv` directory and install the dependencies listed in 
   `pyproject.toml`, including the development dependencies.
3. Either activate the virtual environment manually:

   ```sh
   source .venv/bin/activate
   ```

   or use `uv run <command>` to run commands inside the virtual environment without activating it.

### Shell autocompletion (easy setup)

For a one-time setup of a user-friendly `sparv` command with tab completion (without manually editing shell config), run:

```sh
./scripts/install-shell-completion.sh
```

Or use the Makefile shortcut:

```sh
make completion-install
```

Preview changes without writing to your shell rc file:

```sh
./scripts/install-shell-completion.sh --dry-run
```

Or:

```sh
make completion-install-dry-run
```

Then reload your shell config (zsh example):

```sh
source ~/.zshrc
```

After that, use:

```sh
sparv --help
```

This installs a small wrapper in your shell rc file so you can run `sparv ...` directly while it still uses `uv run` under the hood for this repository.

It also sets a default repo-local data dir:

```sh
SPARV_DATADIR=<repo>/.sparv-data
```

On first-time setup, initialize that data dir once:

```sh
uv run --project . sparv setup --dir "$(pwd)/.sparv-data"
```

Or:

```sh
make completion-setup-datadir
```

If your corpus config uses local custom annotators (e.g. `leitord_og_mark`, `msd_tab_split`, `mmg_metadata`),
install them once into this repo's `.venv`:

```sh
make custom-plugins-install
```

This installs local editable repos from the workspace (including `sparv-leitord-og-mark`
which provides both `leitord_og_mark` and `msd_tab_split`, plus `sparv-mmg-upplysingar`
and local dependencies).

To remove this setup later, run:

```sh
./scripts/uninstall-shell-completion.sh
```

Then reload your shell config again (zsh example):

```sh
source ~/.zshrc
```

Or:

```sh
make completion-uninstall
```

Preview removal without writing changes:

```sh
./scripts/uninstall-shell-completion.sh --dry-run
```

Or:

```sh
make completion-uninstall-dry-run
```

Alternatively, you can set up a virtual environment manually using Python's built-in `venv` module and install the
dependencies using pip:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e . && pip install . --group dev
```

### Running tests

To run the test suite, make sure you have set up the development environment as described above. You also need to have
[Git LFS](https://git-lfs.github.com/) installed to get the test data. If you cloned the repository before installing
Git LFS, you need to run

```sh
git lfs fetch
```

to download the test data files.

While in the Sparv project directory, you can run the tests using uv:

```sh
uv run pytest
```

Alternatively, if you have activated the virtual environment manually, you can simply run:

```sh
pytest
```

You can run specific tests using the provided markers (e.g. `pytest -m swe` to run the Swedish tests only) or via
substring matching (e.g. `pytest -k "not slow"` to skip the slow tests).
