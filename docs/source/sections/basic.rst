Basic Usage
===========

To use ecstasy, you mark up a standard Python string using ecstasy's special syntax, chose some sassy styling and formatting flags, pass them on to the package-level beautify() method and, in return, get your beautified string, ready to kick ass when printed to your command-line:

.. code-block:: python

	import ecstasy

	text = "<Cats> are <0>just> <<small>, furry <elephants>>!"

	text = ecstasy.beautify(text,
							ecstasy.Style.Blink | ecstasy.Color.Red,
							ecstasy.Style.Bold | ecstasy.Fill.Blue,
							ecstasy.Color.Magenta | ecstasy.Style.Underline,
							small=ecstasy.Style.Invert | ecstasy.Color.White)

	print(text)

Running this in a script from a command-line outputs:

.. image:: https://github.com/goldsborough/ecstasy/docs/img/usage.gif
	:alt: Badassery