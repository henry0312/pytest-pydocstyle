from setuptools import setup


setup(
    name='pytest-docstyle',
    version='1.2.0',
    description='pytest plugin to run pydocstyle',
    url='https://github.com/henry0312/pytest-docstyle',
    author='Tsukasa OMOTO',
    author_email='henry0312@gmail.com',
    license='MIT',
    py_modules=['pytest_docstyle'],
    python_requires='>=3.6,<4',
    install_requires=[
        'pytest>=3.3,<3.4',
        'pydocstyle>=2.1,<2.2',
    ],
    # https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others
    entry_points = {
        'pytest11': [
            'docstyle = pytest_docstyle',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Framework :: Pytest',
    ],
)
