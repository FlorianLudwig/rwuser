from setuptools import setup


config = {
    'name': 'rwuser',
    'author': 'Florian Ludwig',
    'version': '0.0.1',
    'install_requires': ['pytest', 'perm', 'fpt'],
    'packages': ['rwuser'],
    'entry_points': {
        'console_scripts': [
            'rwuser = rwuser.cli:main',
        ],
    },
    'license': "http://www.apache.org/licenses/LICENSE-2.0",
    'classifiers': [
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
}

setup(**config)
