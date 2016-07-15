import os

from setuptools import setup, find_packages
from subprocess import check_output, CalledProcessError

VERSION = '2.0.0'
ISRELEASED = False

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

install_requires = [
    line.strip() for line in open(os.path.join(here, 'requirements.txt'))
    ]

scripts = [
    'scripts/iCount',
]

classifiers = [
    'Development Status :: 4 - Beta',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Operating System :: POSIX',
    'Programming Language :: Python',
]


if not ISRELEASED:
    # get version tag from git and store to iCount/_version.py
    try:
        # get version from github
        version = check_output('git describe --tags --long --dirty'.split())
        version = version.decode('utf-8').strip()
        parts = version.split('-')
        assert len(parts) in (3, 4)
        dirty = len(parts) == 4
        tag, count, sha = parts[:3]
        if count == '0' and not dirty:
            version = tag
        else:
            version = "{tag}.dev{ccount}+{gitsha}".format(
                tag=tag,
                ccount=count,
                gitsha=sha.lstrip('g'),
            )
            if dirty:
                version += "dirty"
        VERSION = version
    except (CalledProcessError, FileNotFoundError) as e:
        print('Could not query git: {0}'.format(e))
        print('Please, add a proper version file: iCount/_version.py')

# store version to file
open('iCount/_version.py', 'w').write(
    "# THIS FILE WAS GENERATED BY SETUP.PY\n"
    "__version__ = '{}'\n".format(VERSION))

setup(name='iCount',
      version=VERSION,
      description='Computational pipeline for analysis of iCLIP data',
      long_description=README + '\n\n' + CHANGES,
      classifiers=classifiers,
      author='University of Ljubljana, Bioinformatics Laboratory',
      author_email='tomazc@gmail.com',
      url='',
      keywords='iCLIP protein-RNA',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      test_suite='iCount.tests.suite',
      scripts=scripts,
      )