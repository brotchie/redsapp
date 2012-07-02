#!/usr/bin/env python

__version__ = '0.1'

from setuptools import setup, find_packages, findall

def include_data_files(*paths):
    return [('share/' + path, findall(path)) for path in paths]

setup(name="redsapp",
      version=__version__,
      description="Prototype application for coaching management.",
      author="Factorial Products Pty. Ltd.",
      author_email="brotchie@gmail.com",
      url="http://coaching.factorialproducts.com/",
      packages=['redsapp'],
      package_data={'redsapp': ['templates/*']},
      data_files=include_data_files('static', 'utils', 'rum'),
      zip_safe=False,
      entry_points="""
      [paste.app_factory]
      main = redsapp.web:build_application
      """
)
