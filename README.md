<p align="center">
<img src="https://github.com/dobraczka/recite/raw/main/docs/assets/logo.png" alt="recite logo", width=200/>
</p>
<h2 align="center"> recite</h2>


<p align="center">
<a href="https://github.com/dobraczka/recite/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/recite/actions/workflows/main.yml/badge.svg?branch=main"></a>
<a href='https://recite.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/recite/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://codecov.io/gh/dobraczka/kiez"><img src="https://codecov.io/gh/dobraczka/kiez/branch/main/graph/badge.svg?token=AHBYFKJVLV"/></a>
<a href="https://pypi.org/project/recite"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/recite"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

`recite` intends to make releasing [poetry](https://python-poetry.org/)-based libraries easier and avoid missing important steps (e.g. adapting the changelog).

It checks the following steps:
    - Make sure you have a (non-empty) pyproject.toml
    - Make sure you're on main/master branch
    - Make sure git is clean
    - Run test-suite
    - Make sure changelog was updated (because [you should keep one](https://keepachangelog.com/))

If this succeeds, it performs the following steps:
    - Bump the version via poetry's [version](https://python-poetry.org/docs/cli/#version) command
    - Add and commit the changed pyproject.toml
    - Create a git tag with the new version
    - Push the new tag
    - Publish (and build) via poetry's [publish](https://python-poetry.org/docs/cli/#publish) command
    - Reminds you to create a github relase with release information from your changelog

Usage
=====

Installation
============
