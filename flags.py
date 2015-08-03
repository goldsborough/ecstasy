from enum import Enum, unique

limit = 0

class Hack:
	last = None
	start = 1

class MetaEnum(Enum):
	def __new__(cls, code):
		global limit

		# Set the start of bit shifting to 
		# the last value of the last enum
		if cls is not Hack.last:
			if Hack.last:
				Hack.start = list(Hack.last)[-1].value << 1
			Hack.last = cls

		obj = object.__new__(cls)
		obj._value_ = Hack.start << len(cls.__members__)
		obj.code = code

		limit = obj._value_ << 1

		return obj

	def __int__(self):
		return self.value

	def __str__(self):
		return str(self.code)

	def __or__(self, other):
		return self.value | other.value

	def __ror__(self, other):
		return self.value | other

	def __and__(self, other):
		return self.value & other.value	

	def __rand__(self, other):
		return other & self.value

@unique
class Format(MetaEnum):
	Reset = (0)
	Bold = (1)
	Dim = (2)
	Underline = (4)
	Blink = (5)
	Invert = (7)
	Hidden = (8)

@unique
class Color(MetaEnum):

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