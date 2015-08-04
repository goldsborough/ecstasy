from . import parser
from .flags import Color, Fill, Format

def beautify(text, *args, **kwargs):
	p = parser.Parser(args, kwargs)
	return p.beautify(text)
	