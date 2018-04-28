import os
from setuptools import setup, find_packages
from uaebackend import __version__


def readme():
    with open('README.md') as f:
        return f.read()


def get_abs_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


# we only want to put production dependencies in our egg manifest
install_requires = []
tests_requires = []
with open(get_abs_path('requirements.txt')) as fh:
    capture = install_requires
    for line in fh.readlines():
        if line.startswith('#'):
            if 'tests' in line.lower():
                capture = tests_requires
            continue
        capture.append(line.strip())


setup(name='uaebackend',
      version=__version__,
      description='uaebackend',
      long_description=readme(),
      author='Jean Jacobi',
      author_email='jjacobi@sutdent.42.fr',
      license='Contact Author Please',
      packages=find_packages(),
      include_package_data=True,
      test_suite='tests',
      keywords=['uae', 'challenge', 'arabic', 'backend'],
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_requires,
      extras_require={'test': tests_requires}
      )
