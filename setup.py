#!/usr/bin/env python

import sys, os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

classifiers = [
               'Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'Intended Audience :: Science/Research',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Scientific/Engineering :: GIS',
               ]

setup(name='vectorformats',
      version='0.2',
      description='geographic data serialization/deserialization library',
      long_description=read('doc/Readme.txt'),
      author='VectorFormats (iocast)',
      author_email='vectorformats@live.com',
      url='http://featureserver.org/vectorformats.html',
      
      #packages=['vectorformats',
      #          'vectorformats.formats',
      #          'vectorformats.lib'],
      packages=find_packages(exclude=["doc", "tests"]),
      
      install_requires=['dxfwrite>=1.2.0',
                        'simplejson>=2.6.2',
                        'pyspatialite>=3.0.1',
                        'pyshp>=1.1.4',
                        'Cheetah>=2.4.4'],

      test_suite = 'tests.test_suite',
      
      zip_safe=False,
      license="MIT",
      classifiers=classifiers
      )
