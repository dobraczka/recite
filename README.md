<p align="center">
<img src="https://github.com/dobraczka/recite/raw/main/docs/assets/logo.png" alt="recite logo", width=200/>
</p>
<h2 align="center"> recite</h2>


<p align="center">
<a href="https://github.com/dobraczka/recite/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/recite/actions/workflows/main.yml/badge.svg?branch=main"></a>
<a href='https://recite.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/recite/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://codecov.io/gh/dobraczka/recite"><img src="https://codecov.io/gh/dobraczka/recite/branch/main/graph/badge.svg?token=TCMKS9U0MH"/></a>
<a href="https://pypi.org/project/recite"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/recite"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

`recite` intends to make releasing [poetry](https://python-poetry.org/)-based libraries easier and avoid missing important steps (e.g. adapting the changelog (because [you should keep one](https://keepachangelog.com/))).

```console
$ recite release patch

recite > 👀 Checking everything to make sure you are ready to release 👀
recite > 1: ✓ Make sure you have a (non-empty) pyproject.toml
recite > 2: ✓ Make sure you're on main/master branch
recite > 3: ✓ Make sure git is clean
recite > 4: ✓ Run test-suite
recite > 5: ✓ Make sure changelog was updated
recite > 🤓 Everything looks perfect! 🤓
recite > I will perform the following steps:
recite >        * Would bump version from 0.1.0 to 0.1.1
recite >        * Commit version bump
recite >        * Create git tag 0.1.1
recite >        * Push git tag 0.1.1
recite >        * Remind you to upload build as github release
Do you want to proceed? [y/N]: y
recite > ✨ Performing release ✨
recite > 1: ✓ Bump version
recite >        * Bumped version from 0.1.0 to 0.1.1
recite > 2: ✓ Commit version bump
recite > 3: ✓ Create git tag 0.1.1
recite > 4: ✓ Push git tag 0.1.1
recite > 5: ✓ Build and publish with poetry
Please create a github release now! Did you do it? [y/N]: y
recite > 6: ✓ Remind you to upload build as github release
recite > 🚀 Congrats to your release! 🚀
```

# Installation

Since `recite` is a python application it is recommended to install it via [pipx](https://pypa.github.io/pipx/):
```console
$ pipx install recite
```

But you can also install it via pip:

```console
$ pip install recite
```

# Usage

You can perform e.g a patch release with the command:

```console
$ recite release patch
```

The classifiers are the same as poetry's bump rules of the it's [version command](https://python-poetry.org/docs/cli/#version).

To list the available checks use:

```console
$ recite list-checks
```

You can find more info in the [docs](https://recite.readthedocs.io)

# Why?

Previously I used a github action to automatically build and publish a new version of a library if a new tag was pushed. However, sometimes I forgot something crucial (e.g. to adapt the changelog). In this case I had to rush to stop the github action before it would publish the release to pypi (where it would lie forever unable to be rectified).
With `recite` it is ensured all the necessary checks are in place before any tags are created.
