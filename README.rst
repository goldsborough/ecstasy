*******
Ecstasy
*******

Ecstasy is a Python package and markup language that makes your command-line tool so much more beautiful and pretty.

**Your command-line tool's output without ecstasy:**

.. image:: https://github.com/goldsborough/ecstasy/docs/img/without.png
	:alt: Y U NO WORK?!

**Your command-line tool's output with (on?) ecstasy:**

.. image:: https://github.com/goldsborough/ecstasy/docs/img/with.gif
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
							ecstasy.Style.Blink | ecstasy.Color.Red,
							ecstasy.Style.Bold | ecstasy.Fill.Blue,
							ecstasy.Color.Magenta | ecstasy.Style.Underline,
							small=ecstasy.Style.Invert | ecstasy.Color.White)

	# Keyword arguments (small=...) cause all phrases matching the string of
	# the key to have the style specified by the keyword argument's value.

	print(text)

Running this in a script from a command-line outputs:

.. image:: https://github.com/goldsborough/ecstasy/docs/img/usage.gif
	:alt: Badassery

Installation
============

Now that you're convinced, you can install ecstasy with pip:::

	pip install ecstasy

... and get crackin'.

Documentation
=============

Full documentation and usage descriptions specifying all possible options and possibilities of how you can beautify your strings with *ecstasy* can be found `here <http://ecstasy.readthedocs.org/en/latest/>`_.

Compatibility
=============

According to `pyqver <https://github.com/ghewgill/pyqver/>`_, the minimum required Python version is 2.6. Definitely successfully tested with Python 2.7.10 and Python 3.4.3.

License
=======

Ecstasy is released under the MIT license (see the LICENSE file).

Authors
=======

Peter Goldsborough + cat.