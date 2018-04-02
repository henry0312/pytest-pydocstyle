# pytest-docstyle

[![PyPI version](https://badge.fury.io/py/pytest-docstyle.svg)](https://pypi.org/project/pytest-docstyle/)

[pytest](https://docs.pytest.org/en/latest/) plugin to run [pydocstyle](https://github.com/PyCQA/pydocstyle)

## Installation

```sh
pip install pytest-docstyle
```

## Usage

```sh
pytest --docstyle ...
```

For detail, please see `pytest -h` after installation.

## Configuration

You can configure options of pydocstyle with `setup.cfg` (or `pytest.ini`).  
(cf. [Configuration — pytest documentation](https://docs.pytest.org/en/latest/customize.html))

For example,

```
[tool:pytest]
docstyle_convention = numpy
docstyle_add_ignore = D400 D403
```

## Licence

The MIT License  
Copyright (c) 2017 Tsukasa OMOTO

## Acknowledgments

- [abendebury/pytest-pep257](https://github.com/abendebury/pytest-pep257)
