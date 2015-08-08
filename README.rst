.. raw:: html
	
	<div align="center">
	<h1>
		<span style="color: #2F2BAD">E</span>
		<span style="color: #AD2BAD">c</span>
		<span style="color: #E42692">s</span>
		<span style="color: #F71568">t</span>
		<span style="color: #F7DB15">a</span>
		<span style="color: #2F2BAD">s</span>
		<span style="color: #AD2BAD">y</span>
	</h1>
	<br>
	<a href='https://travis-ci.org/goldsborough/ecstasy'>
		<img src='https://travis-ci.org/goldsborough/ecstasy.svg?branch=master?branch=master'/>
	</a>
	<a href='https://codeclimate.com/github/goldsborough/ecstasy'>
		<img src='https://codeclimate.com/github/goldsborough/ecstasy/badges/gpa.svg'/>
	</a>
	<a href='http://goldsborough.mit-license.org'>
		<img src='https://img.shields.io/github/license/mashape/apistatus.svg'/>
	</a>
	<a href='http://badge.fury.io/py/ecstasy'>
		<img src='https://badge.fury.io/py/ecstasy.svg'/>
	</a>
	<a href='https://coveralls.io/github/goldsborough/ecstasy?branch=master'>
		<img src='https://coveralls.io/repos/goldsborough/ecstasy/badge.svg?branch=master&service=github?branch=master&service=github'/>
	</a>
	<a href='http://img.shields.io/gratipay/goldsborough'>
		<img src='http://img.shields.io/gratipay/goldsborough.svg'/>
	</a>
	</div>

\

Ecstasy is here to make your command-line tool beautiful and fancy.

**Your command-line tool's output without ecstasy:**

.. image:: https://github.com/goldsborough/ecstasy/blob/master/docs/img/without.png
	:alt: Y U NO WORK?!

\

**Your command-line tool's output with (on?) ecstasy:**

.. image:: https://github.com/goldsborough/ecstasy/blob/master/docs/img/with.gif
	:alt: Y U NO WORK?!

Usage
=====

To use ecstasy, you mark up a standard Python string using ecstasy's special syntax, chose some sassy styling and formatting flags, pass them on to the package-level beautify() method and, in return, get your beautified string, ready to kick ass when printed to your command-line:

.. code-block:: python

	import ecstasy

	# <...> is a normal phrase, its style is determined by its position
	# <(x)...> is a phrase with an argument, its style is the one at index 'x'
	# <<...> <...>> is a phrase with nested phrases, their styles cascade
	text = "<Cats> are <(0)just> <<small>, furry <elephants>>!"

	# Beautify text by specifying styles via flag combinations
	text = ecstasy.beautify(text,
				ecstasy.Style.Blink   | ecstasy.Color.Red,
				ecstasy.Style.Bold    | ecstasy.Fill.Blue,
				ecstasy.Color.Magenta | ecstasy.Style.Underline,
				small=ecstasy.Style.Invert | ecstasy.Color.White)

	# Keyword arguments (small=...) cause all phrases matching the string of
	# the key to have the style specified by the keyword argument's value.

	print(text)

Running this in a script from a command-line outputs:

.. image:: https://github.com/goldsborough/ecstasy/blob/master/docs/img/usage.gif
	:alt: Badassery

Installation
============

Now that you're convinced, you can install ecstasy with pip:

::

	pip install ecstasy

... and get crackin'.

`Documentation <http://ecstasy.readthedocs.org/en/latest/>`_
============================================================

Full documentation and usage descriptions specifying all possible options and possibilities of how you can beautify your strings with *ecstasy* can be found `here <http://ecstasy.readthedocs.org/en/latest/>`_.

Compatibility
=============

Python Versions
---------------

Built with Python 3.4 and Python 2.7. Additionally successfully backported to and tested with Python 2.6, 3.2 and also 3.3.

Terminal Support
----------------

Works out of the box with your Mac's terminal. For more information, please enjoy this table:

==========  ====  ===  ==========  =====  ======  ======  =====
Terminal    Bold  Dim  Underlined  Blink  Invert  Hidden  Color
==========  ====  ===  ==========  =====  ======  ======  =====
aTerm        ✓     X       ✓        X       ✓       X       ✓
Eterm       (\1)   X       ✓        X       ✓       X       ✓
GNOME        ✓     ✓       ✓        X       ✓       ✓       ✓
Guake        ✓     ✓       ✓        X       ✓       ✓       ✓
Konsole      ✓     X       ✓        ✓       ✓       X       ✓
Nautilus     ✓     ✓       ✓        X       ✓       ✓       ✓
rxvt         ✓     X       ✓       (\2)     ✓       X       ✓
Terminator   ✓     ✓       ✓        X       ✓       ✓       ✓
Tilda        ✓     X       ✓        X       ✓       X       ✓
XFCE4        ✓     ✓       ✓        X       ✓       ✓       ✓
XTerm        ✓     X       ✓        ✓       ✓       ✓       ✓
xvt          ✓     X       ✓        X       ✓       X       X
Linux TTY    ✓     X       X        X       ✓       X       ✓
VTE          ✓     ✓       ✓        X       ✓       ✓       ✓
==========  ====  ===  ==========  =====  ======  ======  =====

\

(\1) Lighter colors instead of bold.

(\2) Lighter colors instead of blink.

`License <http://goldsborough.mit-license.org>`_
================================================

Ecstasy is released under the `MIT license <http://goldsborough.mit-license.org>`_.

Authors
=======

Peter Goldsborough & `cat <https://goo.gl/IpUmJn>`_ :heart:
