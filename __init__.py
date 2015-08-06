"""
Provides an outside-world (user) interface to the ecstasy package.
"""

from . import parser
from .flags import Color, Fill, Style

def beautify(string, *args, **kwargs):
	"""
		Interfacing-method to the ecstasy package.

		Arguments:
			string (str): The string to beautify with ecstasy.
			args (list): The positional arguments.
			kwargs (dict): The keyword ('always') arguments.
	"""

	p = parser.Parser(args, kwargs)
	return p.beautify(string)
	