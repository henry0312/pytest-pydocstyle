import os

from setuptools import setup

if os.environ.get('BUILD', None):
    packages = ['pytest-docstyle', 'pytest-pydocstyle']
else:
    packages = ['pytest-docstyle']

for name in packages:
    setup(
        name=name,
        version='1.3.0',
        description='pytest plugin to run pydocstyle',
        url='https://github.com/henry0312/pytest-docstyle',
        author='Tsukasa OMOTO',
        author_email='henry0312@gmail.com',
        license='MIT',
        py_modules=['pytest_docstyle'],
        python_requires='~=3.5',
        install_requires=[
            'pytest>=3.0,<4',
            'pydocstyle>=2.1,<2.2',
        ],
        extras_require={
            'tests': [
                'pytest-codestyle>=1.0,<2.0',
                'pytest-isort>=0.1,<1.0',
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
