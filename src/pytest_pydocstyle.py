# https://docs.pytest.org/en/latest/writing_plugins.html
# https://docs.pytest.org/en/latest/example/nonpython.html#yaml-plugin

import contextlib
import logging
import pathlib
import sys

import pydocstyle
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('pydocstyle')
    group.addoption('--pydocstyle', action='store_true',
                    default=False, help='run pydocstyle')


def pytest_configure(config):
    config.addinivalue_line('markers', 'pydocstyle: mark tests to be checked by pydocstyle.')


# https://github.com/palantir/python-language-server/blob/0.30.0/pyls/plugins/pydocstyle_lint.py#L110
# LICENSE: https://github.com/palantir/python-language-server/blob/0.30.0/LICENSE
@contextlib.contextmanager
def _patch_sys_argv(arguments):
    old_args = sys.argv

    # Preserve argv[0] since it's the executable
    sys.argv = old_args[0:1] + arguments

    try:
        yield
    finally:
        sys.argv = old_args


def pytest_collect_file(file_path: pathlib.Path, path, parent):
    """Create a Collector for the given path, or None if not relevant.

    See:
      - https://docs.pytest.org/en/7.0.x/reference/reference.html#pytest.hookspec.pytest_collect_file
    """
    config = parent.config
    if config.getoption('pydocstyle') and file_path.suffix == '.py':
        parser = pydocstyle.config.ConfigurationParser()
        args = [file_path.name]
        with _patch_sys_argv(args):
            parser.parse()
        for filename, _, _ in parser.get_files_to_check():
            return File.from_parent(parent=parent, path=file_path, config_parser=parser)


class File(pytest.File):

    @classmethod
    def from_parent(cls, parent, path: pathlib.Path, config_parser: pydocstyle.config.ConfigurationParser):
        # https://github.com/pytest-dev/pytest/blob/3e4c14bfaa046bcb5b75903470accf83d93f01ce/src/_pytest/nodes.py#L624
        _file = super().from_parent(parent=parent, path=path)
        # store config parser of pydocstyle
        _file.config_parser = config_parser
        return _file

    def collect(self):
        # https://github.com/pytest-dev/pytest/blob/3e4c14bfaa046bcb5b75903470accf83d93f01ce/src/_pytest/nodes.py#L524
        yield Item.from_parent(parent=self, name=self.name, nodeid=self.nodeid)


class Item(pytest.Item):
    CACHE_KEY = 'pydocstyle/mtimes'

    def __init__(self, name, parent, nodeid):
        # https://github.com/pytest-dev/pytest/blob/ee1950af7793624793ee297e5f48b49c8bdf2065/src/_pytest/nodes.py#L544
        super().__init__(name, parent=parent, nodeid=f"{nodeid}::PYDOCSTYLE")
        self.add_marker('pydocstyle')
        # load config parser of pydocstyle
        self.parser: pydocstyle.config.ConfigurationParser = self.parent.config_parser

    def setup(self):
        if not hasattr(self.config, 'cache'):
            return

        old_mtime = self.config.cache.get(self.CACHE_KEY, {}).get(str(self.fspath), -1)
        mtime = self.fspath.mtime()
        if old_mtime == mtime:
            pytest.skip('previously passed pydocstyle checks')

    def runtest(self):
        pydocstyle.utils.log.setLevel(logging.WARN)  # TODO: follow that of pytest

        # https://github.com/PyCQA/pydocstyle/blob/4.0.1/src/pydocstyle/cli.py#L42-L45
        for filename, checked_codes, ignore_decorators in self.parser.get_files_to_check():
            errors = [str(error) for error in pydocstyle.check((str(self.fspath),), select=checked_codes,
                                                               ignore_decorators=ignore_decorators)]
        if errors:
            raise PyDocStyleError('\n'.join(errors))
        elif hasattr(self.config, 'cache'):
            # update cache
            # http://pythonhosted.org/pytest-cache/api.html
            cache = self.config.cache.get(self.CACHE_KEY, {})
            cache[str(self.fspath)] = self.fspath.mtime()
            self.config.cache.set(self.CACHE_KEY, cache)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(PyDocStyleError):
            return excinfo.value.args[0]
        else:
            return super().repr_failure(excinfo)

    def reportinfo(self):
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/main.py#L550
        # https://github.com/pytest-dev/pytest/blob/4678cbeb913385f00cc21b79662459a8c9fafa87/_pytest/doctest.py#L149
        return self.fspath, None, 'pydocstyle-check'


class PyDocStyleError(Exception):
    """custom exception for error reporting."""
