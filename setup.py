from setuptools import setup

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
      install_requires=[
      ],
)

