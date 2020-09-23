"""Setuptools for HFormat"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_descr = (here / "README.md").read_text(encoding="utf-8")
setup(
      name = "morelib",
      version = "0.1.0",
      description = "Extra general-purpose features for Python",
      long_description = long_descr,
      long_description_content_type = "text/markdown",
      url = "https://github.com/angmorpri/morelib",
      author = "Ángel Moreno",
      author_email = "angelmorenoprieto@gmail.com",
      license = "MIT",
      classifiers = [
      	'Development Status :: 4 - Beta',
      	'License :: OSI Approved :: MIT License',
      	'Programming Language :: Python :: 3',
      	'Topic :: Utilities',
      ],
      keywords = "extra, util, utils, more",
      python_requires = ">=3.6, <4",
      packages = find_packages(),
      #package_data = {},
)
