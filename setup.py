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
    author='OMOTO Tsukasa',
    author_email='tsukasa@oomo.to',
    license='MIT',
    py_modules=['pytest_pydocstyle'],
    python_requires='~=3.6',
    install_requires=[
        'pytest~=5.4',
        'pydocstyle',
    ],
    extras_require={
        'tests': [
            'pytest-codestyle~=2.0',
            'pytest-isort',
        ],
    },
    # https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others
    entry_points={
        'pytest11': [
            'pydocstyle = pytest_pydocstyle',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Framework :: Pytest',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
