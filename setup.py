import sys
from setuptools import setup

# this is straight from the py.test website
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name="filecleaver",
      version="0.9.0",
      scripts=[],
      packages=["filecleaver"],
      description="Cleave (split) files on line boundaries.",
      long_description="Cleave (split) files on line boundaries.",
      classifiers=["Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Topic :: Text Processing :: General",
      ],
      keywords="split file",
      author="Brent Woodruff",
      author_email="brent@fprimex.com",
      url="http://github.com/fprimex/filecleaver",
      license="Apache",
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      tests_require = ['pytest'],
      cmdclass = {'test': PyTest},
      test_suite = "tests",
)

