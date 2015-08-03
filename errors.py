"""
Custom error classes and a method to retrieve the line
and column of a character with a (multi-line) string.
"""

class ParseError(Exception):
	"""
	Raised when the string passed to the beautify()
	method is ill-formed and includes some syntactic
	badness such as missing closing tags.

	Attributes:
		what (str): A descriptive string regarding the cause of the error.
	"""

	def __init__(self, what):
		"""
		Initializes the 'what' attribute and the Exception super-class.
		"""

		self.what = what

		super(ParseError, self).__init__(what)

class ArgumentError(Exception):
	"""
	Raised when the positional argument for a phrase
	is either out-of-range (i.e. there were fewer positional
	arguments passed to beautify() than requested in the
	argument) or if it is just total nonsense (i.e. not a
	digit referring to a position and not the escape character).

	Attributes:
		what (str): A descriptive string regarding the cause of the error.
	"""

	def __init__(self, what):
		"""
		Initializes the 'what' attribute and the Exception super-class.
		"""

		self.what = what
		super(ArgumentError, self).__init__(what)

class InternalError(Exception):
	"""
	Raised when something went wrong internally, i.e.
	within methods that are non-accessible via the
	API but are used for internal features or processing.
	Basically get mad at the project creator.

	Attributes:
		what (str): A descriptive string regarding the cause of the error.
	"""

	def __init__(self, what):
		"""
		Initializes the 'what' attribute and the Exception super-class.
		"""

		self.what = what
		super(InternalError, self).__init__(what)

def position(string, index):
	"""
	Returns a helpful position description for an index in a
	(multi-line) string using the format line:column.

	Arguments:
		string: The string to which the index refers.
		index: The index of the character in question.

	Returns:
		A string with the format line:column where line refers to the
		1-indexed row/line in which the character is found within the
		string and column to the position of the character within
		(relative to) that  line.
	"""

	if index < 0 or index >= len(string):
		raise InternalError("Out-of-range index passed to position()!")

	before = 0

	for n, line in enumerate(string.split("\n")):
		# Note that we really want > and not
		# >= because the length is 1-indexed
		# while the index is not, i.e. the
		# value of 'before' already includes the
		# first character of the next line when
		# speaking of its 0-indexed index
		if before + len(line) > index:
			break
		before += len(line)

	# n + 1 to have it 1-indexed
	# index - before to have only the
	# index within the relevant line
	return "{}:{}".format(n + 1, index - before)
