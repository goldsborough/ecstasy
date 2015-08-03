from . import parser
from .flags import Color, Fill, Format

def beautify(text, *args, **kwargs):
	return parser.beautify(text, args, kwargs)