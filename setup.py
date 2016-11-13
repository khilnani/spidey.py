#! /usr/bin/env python
#! -*- coding: utf-8 *-*-

from setuptools import setup, find_packages

readme = open('README.md', 'r').read()
setup(
    name='badspider',
    version='0.1',
    url='https://github.com/khilnani/badspider.py',
    license='MIT',
    author='khilnani',
    author_email='nik@khilnani.org',
    description='Terrible web spider, but useful for recursive API downloads.',
    include_package_data=True,
    long_description=readme,
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'badspider = badspider:main',
            ]
    },
    keywords=('web', 'api', 'downloader', 'spider', 'crawler'),
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],  
    ) 