#!/usr/bin/env python

from distutils.core import setup
from pkgutil import walk_packages

import pylepton

def find_packages(path=".", prefix=""):
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name

setup(name='pylepton',
      version='0.1.2',
      description='FLIR Lepton 3 interface library for Python',
      author='Nathan Lam',
      author_email='nathancy@hawaii.edu',
      url='https://github.com/nathancy/flir_lepton_sensor',
      packages = list(find_packages(pylepton.__path__, pylepton.__name__)),
      scripts = ['../scripts/capture.py', '../scripts/overlay.py'],
      install_depends = ['numpy', 'cv2'],
     )
