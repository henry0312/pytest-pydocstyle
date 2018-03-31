# pytest-pydocstyle

[![PyPI version](https://badge.fury.io/py/pytest-pydocstyle.svg)](https://pypi.org/project/pytest-pydocstyle/)

[pytest](https://docs.pytest.org/en/latest/) plugin to run [pydocstyle](https://github.com/PyCQA/pydocstyle)

## Installation

```sh
pip install pytest-pydocstyle
```

## Usage

```sh
pytest --pydocstyle ...
```

For detail, please see `pytest -h` after installation.

## Configuration

The behavior can be configured in the same style of pydocstyle.  
(cf. [Configuration — pytest documentation](https://docs.pytest.org/en/latest/customize.html) and [Configuration Files — pydocstyle documentation](http://www.pydocstyle.org/en/latest/usage.html#configuration-files))

For example,

```
[pydocstyle]
convention = numpy
add-ignore = D400,D403

[tool:pytest]
addopts = --pydocstyle
```

## Licence

The MIT License  
Copyright (c) 2019 OMOTO Tsukasa

## Acknowledgments

- [abendebury/pytest-pep257](https://github.com/abendebury/pytest-pep257)
