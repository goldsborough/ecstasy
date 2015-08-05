"""
Formatting and style flags for ecstasy.

The MIT License (MIT)

Copyright (c) 2015 Peter Goldsborough

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without LIMITation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from enum import Enum, unique

LIMIT = 0

class Hack(object):
	"""
	A hack namespace to make enumeration work continuously
	across multiple flag enum-classes. 'last' will be
	set to the last enumerated enum-class and
	start to the value at which the flag values
	of the enum-class currently being evaluated
	in the MetaEnum.__new__() method start (i.e. start
	is the flag value of the previous enum-class left-
	shifted by one bit).
	"""

	last = None
	start = 1

class MetaEnum(Enum):

	"""
	Base class for all flag enum-classes as well as the
	individual flag objects/enum members inside the classes
	(by virtue of the enum.Enum semantics).

	The most important re-defined method is __new__ which initializes
	a flag with a command-line format/style escape-code specific to
	the flag, as well as with a numeric value (power of 2) that
	depends on its position inside the enum-class and also on the
	position of the enum-class itself inside the order of enum
	classes (as the Hack mechanism will continuously increment
	flag values over multiple MetaEnum sub-enum-classes). This class
	also defines various necessary operator and conversion overloads
	that define the semantics/interaction of flags (such as that
	you can bitwise-OR and bitwise-AND them).
	"""

	def __new__(cls, code):
		"""
		Constructs a new flag value.

		Apart from constructing a flag via object.__new__,
		this method also sets the flags 'code' attribute
		and its value, which is automatically determined
		by the position of the flag in all enum-classes.
		"""

		global LIMIT

		if cls is not Hack.last:
			if Hack.last:
				# Last flag left shifted by 1 bit
				Hack.start = list(Hack.last)[-1].value << 1
			Hack.last = cls

		obj = object.__new__(cls)
		obj._value_ = Hack.start << len(cls)
		obj.code = code

		LIMIT = obj._value_ << 1

		return obj

	def __int__(self):
		"""
		Converts the flag to its value.

		Returns:
			The integer value stored inside the flag's 'value' attribute.
		"""
		return self.value

	def __str__(self):
		"""
		Turns the flag into its style-code.

		Returns:
			A string version of the flag's style/formatting code.
		"""
		return str(self.code)

	def __or__(self, other):
		"""
		Bitwise-OR operator overload.

		Arguments:
			other (MetaEnum): A flag.

		Returns:
			The combination of the bitwise-OR-ed flags (int).
		"""

		return self.value | other.value

	def __ror__(self, other):
		"""
		Reverse Bitwise-OR operator overload.

		Arguments:
			other (int): An integer value, usually a flag combination.

		Returns:
			The combination of the passed integer and the flag (int).

		"""

		return self.value | other

	def __and__(self, other):
		"""
		Bitwise-OR operator overload.

		Arguments:
			other (MetaEnum): A flag.

		Returns:
			The combination of the bitwise-OR-ed flags (int).
		"""

		return self.value & other.value

	def __rand__(self, other):
		"""
		Reverse Bitwise-AND operator overload.

		Arguments:
			other (int): An integer value, usually a flag combination.

		Returns:
			The result of AND-ing the passed integer and the flag (int).

		"""

		return other & self.value

@unique
class Style(MetaEnum):
	"""
	Special formatting flags pertaining to any style
	alterations that do not involve color (but other
	factors of appearence).
	"""

	Reset = (0)
	Bold = (1)
	Dim = (2)
	Underline = (4)
	Blink = (5)
	Invert = (7)
	Hidden = (8)

@unique
class Color(MetaEnum):
	"""
	Text color flags (not fill-color).
	"""

	Default = (39)
	Black = (30)
	DarkRed = (31)
	DarkGreen = (32)
	DarkYellow = (33)
	DarkBlue = (34)
	DarkMagenta = (35)
	DarkCyan = (36)
	Gray = (37)
	DarkGray = (90)
	Red = (91)
	Green = (92)
	Yellow = (93)
	Blue = (94)
	Magenta = (95)
	Cyan = (96)
	White = (97)

@unique
class Fill(MetaEnum):
	"""
	Fill color flags (not text-color).
	"""

	Default = (49)
	Black = (40)
	DarkRed = (41)
	DarkGreen = (42)
	DarkYellow = (43)
	DarkBlue = (44)
	DarkMagenta = (45)
	DarkCyan = (46)
	Gray = (47)
	DarkGray = (100)
	Red = (101)
	Green = (102)
	Yellow = (103)
	Blue = (104)
	Magenta = (105)
	Cyan = (106)
	White = (107)

def codify(combination):

	"""
	Gets escape-codes for flag combinations.

	Arguments:
		combination (int): Either a single integer-convertible flag
						   or an OR'd flag-combination.
	Returns:
		A semi-colon-delimited string of appropriate escape sequences.
	"""

	codes = []

	for enum in (Style, Color, Fill):
		for flag in enum:
			if combination & flag:
				codes.append(str(flag))

	return ";".join(codes)
