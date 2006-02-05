import sys

sys.path.insert(0, "lib")

from distutils.core import setup

setup(
    name = 'IGEOuterSpaceServer',
    version = '0.5.54',
    description = 'OuterSpace Server',
    author = 'Qark',
    author_email = 'qark@ospace.net',
    url='http://www.sourceforge.net/projects/ospace',
    py_modules = ['run', 'osclient', 'log'],
    packages = ['ige', 'igeclient', 'medusa', 'ige.ospace', 'ige.ospace.Rules'],
)
