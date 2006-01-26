from distutils.core import setup

setup(name='OuterSpaceServer-src',
      version='0.5.54',
      description='OuterSpace Server',
      author='Qark',
      author_email='qark@ospace.net',
      url='http://www.sourceforge.net/projects/ospace',
      py_modules = ['run', 'osclient', 'useradd', 'prof', 'profres', 'lib.log'],
      packages=['lib.ige', 'lib.igeclient', 'lib.medusa', 'lib.ige.ospace', 'lib.ige.ospace.Rules'],
     )
