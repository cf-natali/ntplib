<h1 align="center">ntplib</h1>
<div align="center">An NTP Client for Python</div>
<br />

[![PyPI Status](https://img.shields.io/pypi/v/ntplib.svg)](https://pypi.python.org/pypi/ntplib)
[![Downloads](https://img.shields.io/pypi/dm/ntplib.svg)](https://pypi.python.org/pypi/ntplib)

# Description

This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text
(mode, leap indicator…). Since it’s pure Python, and only depends on core
modules, it should work on any platform with a Python implementation.


# Example

```
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
>>> ntplib.ref_id_to_text(response.ref_id, response.stratum)
193.190.230.66
```

# Installation

```
python setup.py install
```
