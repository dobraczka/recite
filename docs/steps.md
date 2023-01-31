# Steps

## Checks

### (Non-empty) Pyproject.toml

[Poetry](https://python-poetry.org/) uses a `pyproject.toml`, which was introduced in [PEP-518](https://peps.python.org/pep-0518/) to specify build dependencies.

### Deploy while on main

Recite assumes you want to deploy from your local machine and while on the main/master branch of your project.

### Clean git

You should not have modified files, and your local branch should be in sync with the remote.

### Your tests should run without errors

Recite uses [nox](https://nox.thea.codes/en/stable/index.html) as test-suite by default.
For inspiration on what your tests should entail check out the [recommendations](recommendations.md).

### Changelog

You should [keep a changelog](keepachangelog.com/) and recite checks if such a file exists and there is a diff between the current version and the last version tag. Since changelogs are made for human eyes, no fancy checks regarding the contents of the changes are made. 

## Publishing

### Bump version

Uses poetry's [version](https://python-poetry.org/docs/cli/#version) command to bump the version in the `pyproject.toml`.

### Commit bump

Add the modified `pyproject.toml` and commit the change.

### Create tag

Create a new tag with the new version.

### Push tag

Push the newly created tag to the remote.

### Build and publish

Uses poetry's [publish](https://python-poetry.org/docs/cli/#publish) command to build your project and upload it to [PyPI](pypi.org).
If you have `PYPI_TOKEN` as environment variable it will use token-based authentication. Else you will be prompted for the required values.

### Remind you to create a github release

Following the philosophy of a [do-nothing-script](https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/) this step reminds you to create a github release with the build `.whl` and the changes you documented in your changelog.
