import logging
import re

import pydocstyle
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('docstyle')
    group.addoption('--docstyle', action='store_true',
                    default=False, help='run pydocstyle')

    # https://github.com/PyCQA/pydocstyle/blob/2.1.1/src/pydocstyle/config.py#L69
    DEFAULT_MATCH_RE = pydocstyle.config.ConfigurationParser.DEFAULT_MATCH_RE + '$'

    parser.addini('docstyle_convention', default='pep257',
                  help='choose the basic list of error codes to be checked (default: pep257)')
    parser.addini('docstyle_add_select', type='args',
                  help='add error codes')
    parser.addini('docstyle_add_ignore', type='args',
                  help='ignore error codes')
    parser.addini('docstyle_match', default=DEFAULT_MATCH_RE,
                  help='check only files that exactly match'
                       ' regular expression (default: {pattern})'.format(
                           pattern=DEFAULT_MATCH_RE))


def pytest_collect_file(parent, path):
    config = parent.config
    if (config.option.docstyle and path.ext == '.py' \
            # https://github.com/PyCQA/pydocstyle/blob/2.1.1/src/pydocstyle/config.py#L163
            and re.match(config.getini('docstyle_match'), path.basename)):
        return Item(path, parent)


class Item(pytest.Item, pytest.File):
    CACHE_KEY = 'docstyle/mtimes'

    def __init__(self, path, parent):
        super().__init__(path, parent)
        self.add_marker('docstyle')

    def setup(self):
        old_mtime = self.config.cache.get(self.CACHE_KEY, {}).get(str(self.fspath), -1)
        mtime = self.fspath.mtime()
        if old_mtime == mtime:
            pytest.skip('previously passed pydocstyle checks')

    def runtest(self):
        pydocstyle.utils.log.setLevel(logging.WARN)  # TODO: follow that of pytest

        # https://github.com/PyCQA/pydocstyle/blob/de58b1e596a9c64bcd9e82d9ce1cb8a2aeea1f82/src/pydocstyle/config.py#L444
        checked_codes = pydocstyle.violations.conventions[self.config.getini('docstyle_convention')]
        checked_codes |= set(self.config.getini('docstyle_add_select'))
        checked_codes -= set(self.config.getini('docstyle_add_ignore'))

        errors = [str(error) for error in pydocstyle.check([str(self.fspath)], select=checked_codes, ignore=None)]
        if errors:
            raise DocStyleError('\n'.join(errors))
        else:
            # update cache
            # http://pythonhosted.org/pytest-cache/api.html
            cache = self.config.cache.get(self.CACHE_KEY, {})
            cache[str(self.fspath)] = self.fspath.mtime()
            self.config.cache.set(self.CACHE_KEY, cache)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(DocStyleError):
            return excinfo.value.args[0]
        else:
            return super().repr_failure(excinfo)

    def reportinfo(self):
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/main.py#L550
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/doctest.py#L149
        return self.fspath, None, 'pydocstyle-check'


class DocStyleError(Exception):
    """custom exception for error reporting."""
