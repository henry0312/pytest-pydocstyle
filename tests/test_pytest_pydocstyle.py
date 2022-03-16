import pytest_pydocstyle

# https://docs.pytest.org/en/5.2.2/writing_plugins.html#testing-plugins
pytest_plugins = ["pytester"]


def test_option_false(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('pydocstyle')
            assert flag is False
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_option_true(testdir):
    p = testdir.makepyfile("""
        def test_option(request):
            flag = request.config.getoption('pydocstyle')
            assert flag is True
    """)
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--pydocstyle')
    result.assert_outcomes(passed=1)


def test_ini(testdir):
    testdir.makeini("""
        [pydocstyle]
        convention = numpy
        add-ignore = D100
    """)
    p = testdir.makepyfile(a='''
        def hello():
            """Print hello."""
            print('hello')
    ''')
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--pydocstyle')
    result.assert_outcomes(passed=1)


def test_pytest_collect_file(testdir):
    testdir.tmpdir.ensure('a.py')
    testdir.tmpdir.ensure('b.py')
    testdir.tmpdir.ensure('c.txt')
    testdir.tmpdir.ensure('test_d.py')
    result = testdir.runpytest('--pydocstyle')
    # D100: Missing docstring in public module
    result.assert_outcomes(failed=2)


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
    result = testdir.runpytest('--pydocstyle')
    result.assert_outcomes(passed=1, failed=1)
    # second run
    result = testdir.runpytest('--pydocstyle')
    result.assert_outcomes(skipped=1, failed=1)


def test_no_cacheprovider(testdir):
    # D100: Missing docstring in public module
    testdir.tmpdir.ensure('a.py')
    p = testdir.makepyfile(b='''\
        """Test."""
        def hello():
            """Print hello."""
            print('hello')
    ''')
    # first run
    result = testdir.runpytest('--pydocstyle', '-p', 'no:cacheprovider')
    result.assert_outcomes(passed=1, failed=1)
    # second run
    result = testdir.runpytest('--pydocstyle', '-p', 'no:cacheprovider')
    result.assert_outcomes(passed=1, failed=1)


def test_strict(testdir):
    p = testdir.makepyfile(a='''
        """Test strict."""
        def test_blah():
            """Test."""
            pass
    ''')
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('--strict-markers', '--pydocstyle')
    result.assert_outcomes(passed=1)


def test_nodeid(testdir):
    p = testdir.makepyfile(nodeid='''
        """Test _nodeid."""
        def test_nodeid():
            """Test."""
            pass
    ''')
    p = p.write(p.read() + "\n")
    result = testdir.runpytest('-m', 'pydocstyle', '--pydocstyle', '-v')
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(['nodeid.py::PYDOCSTYLE PASSED *'])


class TestItem(object):

    def test_cache_key(self):
        assert pytest_pydocstyle.Item.CACHE_KEY == 'pydocstyle/mtimes'

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


class TestPyDocStyleError(object):

    def test_subclass(self):
        assert issubclass(pytest_pydocstyle.PyDocStyleError, Exception)
