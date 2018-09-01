import pytest_docstyle

# https://docs.pytest.org/en/latest/writing_plugins.html#testing-plugins
pytest_plugins = ["pytester"]


def test_option_false(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('docstyle')
            assert flag is False
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_option_true(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('docstyle')
            assert flag is True
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--docstyle')
    result.assert_outcomes(passed=1)


def test_ini(testdir):
    testdir.makeini("""
        [pytest]
        docstyle_convention = numpy
        docstyle_add_select = a b c
        docstyle_add_ignore = d e f
        docstyle_match = test_re
        docstyle_exclude = exclude.py path/to/another/exclude.py
    """)
    p = testdir.makepyfile("""
        def test_ini(request):
            config = request.config
            select = ['a', 'b', 'c']
            assert config.getini('docstyle_add_select') == select
            ignore = ['d', 'e', 'f']
            assert config.getini('docstyle_add_ignore') == ignore
            match = 'test_re'
            assert config.getini('docstyle_match') == match
            exclude = ['{dirname}/{base}/exclude.py', '{dirname}/{base}/path/to/another/exclude.py']
            assert config.getini('docstyle_exclude') == exclude
    """.format(dirname=testdir.tmpdir.dirname, base=testdir.tmpdir.basename))
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--docstyle')
    result.assert_outcomes(passed=1)


def test_pytest_collect_file(testdir):
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')
    testdir.tmpdir.ensure('c.txt')
    testdir.tmpdir.ensure('test_d.py')
    result = testdir.runpytest('--docstyle')
    result.assert_outcomes(failed=2)


def test_pytest_collect_file_with_exclude(testdir):
    testdir.makeini("""
        [pytest]
        docstyle_exclude = a.py path/to/c.py
    """)
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')
    testdir.tmpdir.ensure('path/to/c.py')
    result = testdir.runpytest('--docstyle')
    result.assert_outcomes(failed=1)


def test_cache(testdir):
    # D100: Missing docstring in public module
    testdir.tmpdir.ensure('a.py')
    p = testdir.makepyfile(b='''\
        """Test."""
        def hello():
            """Print hello."""
            print('hello')
    ''')
    # first run
    result = testdir.runpytest('--docstyle')
    result.assert_outcomes(passed=1, failed=1)
    # second run
    result = testdir.runpytest('--docstyle')
    result.assert_outcomes(skipped=1, failed=1)


class TestItem(object):

    def test_cache_key(self):
        assert pytest_docstyle.Item.CACHE_KEY == 'docstyle/mtimes'

    def test_init(self):
        pass

    def test_setup(self):
        pass

    def test_runtest(self):
        pass

    def test_repr_failure(self):
        pass

    def test_reportinfo(self):
        pass


class TestDocStyleError(object):

    def test_subclass(self):
        assert issubclass(pytest_docstyle.DocStyleError, Exception)
