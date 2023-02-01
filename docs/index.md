# recite

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

<div class="termy">
```console
$ recite patch

recite > 👀 Checking everything to make sure you are ready to release 👀
recite > <span class="termynal-blue-text">1</span>: <span class="termynal-green-text">✓ Make sure you have a (non-empty) pyproject.toml</span>
recite > <span class="termynal-blue-text">2</span>: <span class="termynal-green-text">✓ Make sure you're on main/master branch</span>
recite > <span class="termynal-blue-text">3</span>: <span class="termynal-green-text">✓ Make sure git is clean</span>
recite > <span class="termynal-blue-text">4</span>: <span class="termynal-green-text">✓ Run test-suite</span>
recite > <span class="termynal-blue-text">5</span>: <span class="termynal-green-text">✓ Make sure changelog was updated</span>
recite > 🤓 Everything looks perfect! 🤓
recite > I will perform the following steps:
recite >        * Would bump version from <span class="termynal-yellow-text">0.1.0</span> to <span class="termynal-blue-text">0.1.1</span>
recite >        * Commit version bump
recite >        * Create git tag <span class="termynal-blue-text">0.1.1</span>
recite >        * Push git tag <span class="termynal-blue-text">0.1.1</span>
recite >        * Remind you to upload build as github release

# Do you want to proceed? [y/N]:$ y

recite > ✨ Performing release ✨
recite > <span class="termynal-blue-text">1</span>: <span class="termynal-green-text">✓ Bump version</span>
recite >        <span class="termynal-green-text">* Bumped version from</span> <span class="termynal-yellow-text">0.1.0</span> to <span class="termynal-blue-text">0.1.1</span>
recite > <span class="termynal-blue-text">2</span>: <span class="termynal-green-text">✓ Commit version bump</span>
recite > <span class="termynal-blue-text">3</span>: <span class="termynal-green-text">✓ Create git tag</span> <span class="termynal-blue-text">0.1.1</span>
recite > <span class="termynal-blue-text">4</span>: <span class="termynal-green-text">✓ Push git tag</span> <span class="termynal-blue-text">0.1.1</span>
recite > <span class="termynal-blue-text">5</span>: <span class="termynal-green-text">✓ Build and publish with poetry</span>

# Please create a github release now! Did you do it? [y/N]:$ y

recite > <span class="termynal-blue-text">6</span>: <span class="termynal-green-text">✓ Remind you to upload build as github release</span>
recite > 🚀 Congrats to your release! 🚀
```
</div>

# Installation

Since `recite` is a python application it is recommended to install it via [pipx](https://pypa.github.io/pipx/):


<div class="termy">
```console
$ pipx install recite
---> 100%
Successfully installed recite
```
</div>

But you can also install it via pip

# Why?

Previously I used a github action to automatically build and publish a new version of a library if a new tag was pushed. However, sometimes I forgot something crucial (e.g. to adapt the changelog). In this case I had to rush to stop the github action before it would publish the release to pypi (where it would lie forever unable to be rectified).
With `recite` it is ensured all the necessary checks are in place before any tags are created.
