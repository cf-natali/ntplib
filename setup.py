from distutils.core import setup


long_description = """
ntplib - Python NTP library
===========================

Description
-----------

This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text (mode,
leap indicator...). Since it's pure Python, and only depends on core modules, it
should work on any platform with a Python implementation.

Example
-------

>>> import ntplib
>>> from time import ctime
>>> c = ntplib.NTPClient()
>>> response = c.request('europe.pool.ntp.org', version=3)
>>> response.offset
-0.143156766891
>>> response.version
3
>>> ctime(response.tx_time)
'Sun May 17 09:32:48 2009'
>>> ntplib.leap_to_text(response.leap)
'no warning'
>>> response.root_delay
0.0046844482421875
>>> ntplib.ref_id_to_text(response.ref_id)
193.190.230.66


Installation
------------

As root::

   # python setup.py install

or just copy ntplib.py inside a directory in your sys.path, e.g.
`/usr/lib/python2.5/`.
"""


setup(name='ntplib',
      version='0.3.3',
      description='Python NTP library',
      author='Charles-Francois Natali',
      author_email='cf.natali@gmail.com',
      url='http://code.google.com/p/ntplib/',
      py_modules=['ntplib'],
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: System :: Networking :: Time Synchronization'
      ],
      long_description=long_description
     )
