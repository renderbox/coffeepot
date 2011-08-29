from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='coffeepot',
      version=version,
      description="JavaScript generator for web frameworks",
      long_description="""\
JavaScript generator that can be used in web based frameworks.  Contains tools for the JQuery JS Library and Django.""",
      classifiers=['Development Status :: 2 - Pre-Alpha',
                  'Environment :: Web Environment',
                  'Framework :: Django',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: BSD License',
                  'Operating System :: OS Independent',
                  'Programming Language :: Python',
                  'Topic :: Software Development :: Libraries :: Python Modules',
                  'Topic :: Utilities'], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='web javascript django jquery',
      author='Grant Viklund',
      author_email='renderbox@gmail.com',
      url='http://www.backcode.com',
      license='BSD License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
