import os

from setuptools import setup

version = open('VERSION', 'rb').read().decode('utf-8').strip()
long_description = open('README.md', 'rb').read().decode('utf-8')

setup(
    name='pytest-docstyle',
    version=version,
    description='pytest plugin to run pydocstyle',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/henry0312/pytest-docstyle',
    author='Tsukasa OMOTO',
    author_email='henry0312@gmail.com',
    license='MIT',
    py_modules=['pytest_docstyle'],
    python_requires='~=3.5',
    install_requires=[
        'pytest~=3.0',
        'pydocstyle~=2.1',
    ],
    extras_require={
        'tests': [
            'pytest-codestyle~=1.0',
            'pytest-isort~=0.1',
        ],
    },
    # https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others
    entry_points={
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
