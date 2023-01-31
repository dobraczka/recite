# Recommendations

## Automate your tests

Your code should not only run on _your_ machine. To make sure this is the case you can use tools like [tox](https://christophergs.com/python/2020/04/12/python-tox-why-use-it-and-tutorial/).
Personally, I prefer [nox](https://nox.thea.codes/en/stable/), because it uses standard python files for configuration. 
(And on top of that I also use [nox-poetry](https://github.com/cjolowicz/nox-poetry) to ensure versions from my `poetry.lock` file are respected)

## Test your code

If you use a tool like `recite` you probably do not need somebody to tell you, that you should write tests for your code. I like to use [pytest](https://docs.pytest.org/en/6.2.x/index.html).

## Style-guide

You should ensure your Python code adheres to the style guide according to [PEP 8](https://pep8.org/). To check this you should use [flake8](https://flake8.pycqa.org/en/latest/index.html).
There are a ton of plugins, to enhance this. I like to use the following:

name | description
-----|------------
[flake8-eradicate](https://github.com/wemake-services/flake8-eradicate) | Find commented out or dead code
[flake8-isort](https://github.com/gforcada/flake8-isort) | Check if code is sorted according to [isort](https://github.com/PyCQA/isort)
[flake8-debugger](https://github.com/jbkahn/flake8-debugger) | Check for debugger statements
[flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions) | Write better list/set/dict comprehensions
[flake8-print](https://github.com/JBKahn/flake8-print) | Check for print statements (you should use [logging](https://docs.python.org/3/howto/logging.html) in most cases)
[flake8-black](https://github.com/peterjc/flake8-black) | Check if code is formatted according to [black](https://github.com/psf/black)'s style
[flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) | Find likely bugs and design problems
[darglint](https://github.com/terrencepreilly/darglint) | Check that docstring matches the definition
[pydocstyle](https://github.com/PyCQA/pydocstyle) | Check for compliance with python docstring convention

Since flake8 cannot be configured via `pyproject.toml` I use [pyproject-flake8](https://github.com/csachs/pyproject-flake8) to have all configuration in one place.

Furthermore I use [pyroma](https://github.com/regebro/pyroma) to make sure my project complies with the best practices of the python packaging ecosystem.
