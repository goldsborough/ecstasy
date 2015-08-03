from . import parser
from .flags import Color, Fill, Format

def beautify(text, formats, **always):
	return parser.beautify(text, formats, always)