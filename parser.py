# -*- coding: utf-8 -*-

"""
The heart of the ecstasy package, containing the main Parser class.

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

import re
import warnings
import collections

from . import flags
from . import errors

class Phrase(object):
	"""
	Class describing a single parsed phrase.

	When a string is parsed in ecastasy, specially-marked regions of
	text are converted taken note of and converted into Phrase objects,
	which are later then used to replace the parsed strings (including any
	tags or arguments) with the string itself as well as the formatting
	codes specified by the arguments passed to Parser.beautify(), which
	are then interpreted by the command line.

	Attributes:
		string (str): The text of the phrase (between opening and closing tags).
		opening (int): The index of the opening tag.
		closing (int): The index of the closing tag.
		style (int): The formatting/style flag-combination of the phrase.
		nested (list): A list of nested Phrase objects (children).
		override (bool): The phrase's override specification.
	"""

	def __init__(self,
				 opening=None,
				 closing=None,
				 string=None,
				 style=None):

		self.string = string

		self.opening = opening
		self.closing = closing

		self.style = style

		self.arguments = []

		self.nested = []

		self.override = False

	def __str__(self):
		return self.string

class Parser(object):
	"""
	Handles parsing and beautification of a string.

	This is the main class of the entire ecastasy package. It is
	initialized with a set of positional and keyword arguments that
	determine which styles (flag-combinations) are used for which
	phrases (tag-marked regions of text) found during parsing. Its
	beautify() method is then used to beautify a string according
	to the arguments passed to the constructor.

	Note:
		From the outside, the package-level beautify() method should
		handle the construction and beautify()-call process all-in-one
		(for convenience).

	Attributes:
		always: The list of 'always' (keyword) arguments.
		positional: The list of positional arguments.
		tags: A compiled regex matching opening or closing tags.
		argument: A compiled regex matching well-formed phrase arguments.
		counter: A counter for positional arguments.
	"""

	def __init__(self, args, kwargs):

		"""
		Initializes a Parser instance.

		Arguments:
			args (list): The positional arguments.
			kwargs (dict): The 'always' (keyword) arguments.
		"""

		self.always = kwargs

		self.positional = self.get_flags(args)

		self.tags = re.compile(r"[<>]")

		self.argument = re.compile(r"^(-?\d,?)+!?$")

		# Used in self.stringify to auto-increment
		# positional argument positions
		self.counter = 0

	def get_flags(self, args):

		"""
		Checks and retrieves positional and 'always' (keyword) flags
		from the many ways in which they may be passed to the
		constructor (or the beautify() method on package-level).

		Positional arguments can be passed either:
		- Individually, where each flag-combination is one positional argument.
		- Packaged inside a list, which is then expanded. There can be
		  multiple of such lists passed as arguments because it facilitates
		  interaction with the ecastasy module (one may want to organize
		  and update styles in certain ways depending on one's program), but
		  each list will be expanded and all flag-combinations found inside
		  each list will be interpreted as a single style argument, as if it
		  had been passed in the way desribed above (individually).

		'Always' arguments can be passed either:
		- Individually, with keyword-argument syntax, i.e. <word>=<style>
		- In a dictionary, which is expanded exactly like positional
		  arguments passed in lists (i.e. each key/value pair in the
		  dictionary is interpreted as if it had been passed individually,
		  as key=value to the constructor/the external beautify() method).

		Note:
			self.always is set equal to the kwargs passed to the constructor
			and then modified directly (when 'always'-arguments are found),
			while the positional arguments are put into a list here and
			returned (i.e. no interaction with self.positional).

		Arguments:
			args (list): The positional arguments passed to the constructor.

		Returns:
			The positional arguments.

		Raises:
			errors.FlagError: If an invalid (out-of-range)
							  flag combination was passed.

			errors.EcstasyError: If one of the arguments is of invalid type.

		"""

		positional = []

		for argument in args:
			# A flag is an instance of a subclass of
			# flags.MetaEnum if it was passed alone
			if isinstance(argument, flags.MetaEnum):
				positional.append(argument)

			# or is an integer if it was (bitwise) OR'd
			# with another flag (a "flag combination")
			elif isinstance(argument, int):
				if argument < 0 or argument >= flags.LIMIT:
					raise errors.FlagError("Flag value '{}' is out of range "
										   "!".format(argument))
				positional.append(argument)

			# Dictionaries store 'always'-arguments
			elif isinstance(argument, dict):
				for key, value in argument.items():
					# Simple 'always'-argument where one string
					# is mapped to one formatting flag-combination
					if isinstance(key, str):
						self.always[key] = value

					# Complex 'always'-argument with a
					# tuple containing strings, each with the same
					# flag-combination (same value)
					elif isinstance(key, tuple):
						for i in key:
							self.always[i] = value
					else:
						raise errors.EcstasyError("Key '{}' in dictionary "
												  "argument passed is neither "
												  "a string nor a tuple "
												  "of strings!".format(key))

			elif isinstance(argument, collections.Iterable):
				positional += self.get_flags(argument)

			else:
				raise errors.EcstasyError("Argument '{}' is neither a flag, a "
										  "(bitwise) OR'd flag-combination, a "
										  "dictionary nor an  iterable of "
										  "positional arguments "
										  "!".format(argument))

		return positional

	def beautify(self, string):
		"""
		Wraps together all actions needed to beautify a string, i.e.
		parse the string and then stringify the phrases (replace tags
		with formatting codes).

		Arguments:
			string (str): The string to beautify/parse.

		Returns:
			The parsed, stringified and ultimately beautified string.
		"""

		# string may differ because of escaped characters
		string, phrases = self.parse(string)

		if not phrases:
			return string

		return self.stringify(string, phrases)

	def parse(self, string, root=None):

		"""
		Parses a string to handle escaped tags and retrieve phrases.

		This method works recursively to parse nested tags. When escaped
		tags are found, those are removed from the string. Also argument
		sequences are removed from the string. The string returned can
		thus be quite different from the string passed.

		Arguments:
			string (str): The string to parse.
			root (Phrase): If in a recursive call, the root/parent phrase.

		Returns:
			For one, the escaped string (without escape characters and
			phrase arguments). For the other, it depends on the stack-depth.
			If this is the lowest recursion depth/level (i.e. the stack
			call resulting from the first function call in self.beautify()),
			it will return a list of phrases. For higher stack levels (
			i.e. resulting from recursive function calls from with
			self.parse(), for nested phrases), it returns exactly one
			Phrase instance.

		Raises:
			errors.ParseError: If no closing tag could be
							   found for an opening tag.
		"""

		if not root:
			phrases = []

		tag = self.tags.search(string)

		while tag:

			# Save some function calls
			pos = tag.start()

			if tag.group() == "<":
				string, child, tag = self.open_tag(string, pos)

				if child:
					if root:
						root.nested.append(child)
					else:
						phrases.append(child)

				# else it was escaped (+ new tag)

			# tag is closing ('>')
			elif root:
				string, phrase, tag = self.closing_tag(string, root, pos)

				if phrase:
					return string, phrase

				# else it was escaped (+ new tag)

			else:
				# Replace escape character
				if pos > 0 and string[pos - 1] == "\\":
					string = string[:pos - 1] + string[pos:]
				else:
					# When the phrase is None at the start, there should not
					# be a closing tag because none was ever opened. This is
					# not actually an error, but we should warn about it.
					position = errors.position(string, pos)
					warnings.warn("Un-escaped '>' character at "
							 	  "position {}".format(position),
								  Warning)

				tag = self.tags.search(string, pos + 1)

		if not root:
			return string, phrases

		# If this is not the first stack-depth the function should
		# have returned upon finding a non-argument closing tag,
		# i.e. we should never have gotten here.
		word = re.search(r"([\w\s]+)(?![\d]*>[\w\s]+>)", string)

		raise errors.ParseError("No closing tag found for "
								"opening tag after expression '{}'"
								"!".format(word.group()))

	def open_tag(self, string, pos):

		"""
		Helper function of self.parse() handling opening tags.

		Arguments:
			string (str): The string being parsed.
			pos (int): The index/position of the opening tag in the string.

		Returns:
			The (possibly) escaped string, a child phrase if the opening tag
			was not escaped and otherwise None, and a new tag match, either
			starting at one index passed the escaped tag or one index passed
			the closing tag of the child.
		"""

		# Check for escaping
		if string[pos - 1] == "\\":
			# Remove the escape character
			string = string[:pos - 1] + string[pos:]

			# When removing the escape character, the
			# pos tag index is pushed one back
			pos -= 1

			# If the escape character was not itself (double)
			# escaped we can look for the next tag
			if pos == 0 or string[pos - 1] != "\\":
				tag = self.tags.search(string, pos + 1)

				return string, None, tag

		child = Phrase(pos)

		escaped, child = self.parse(string[pos + 1:], child)

		string = string[:pos + 1] + escaped

		tag = self.tags.search(string, child.closing + 1)

		return string, child, tag

	def closing_tag(self, string, root, pos):

		"""
		Helper function of self.parse() handling closing tags.

		Arguments:
			string (str): The string being parsed.
			root (Phrase): The current root phrase.
			pos (int): The index/position of the closing tag in the string.

		Returns:
			Always the (possibly) escaped string, then either the fully
			formed phrase if the closing tag was not escaped (with its
			'closing' and 'string' attributes set) and otherwise None,
			and lastly the next tag if the closing tag was indeed escaped
			and otherwise None -- i.e. either the tuple
			(string, phrase, None) or (string, None, tag).
		"""

		# Whatever is between the opening tag and this closing tag
		substring = string[:pos]

		# Positional argument <^(-?\d,?)+$>
		if self.argument.match(substring):

			# Override mode (overrides 'always' style)
			if substring.endswith("!"):
				root.override = True
				substring = substring[:-1]

			root.arguments = [int(i) for i in substring.split(",")]

			string = string[pos + 1:]

			tag = self.tags.search(string)

			return string, None, tag

		# Escape-character to escape the closing tag (/>)
		elif substring.endswith("\\"):

			# Get rid of the escape character either way
			string = string[:pos - 1] + string[pos:]

			# Check if not double-escaped
			if not substring[:-1].endswith("\\"):
				# pos is now one index passed the closing tag
				tag = self.tags.search(string, pos)

				return string, None, tag

			# Double-escape means this is really supposed to be a
			# closing tag and thus we can return the phrase.
			else:
				# The closing position should be in the same scope
				# as the scope of the opening position (scope in
				# the sense of to which phrase the positions are
				# relative to). -1 due to the escaped character but
				# + 1 because index 0 is phrase.opening + 1
				root.closing = root.opening + pos
				root.string = string[:pos - 1]
		else:
			root.closing = root.opening + 1 + pos
			root.string = string[:pos]

		return string, root, None

	def stringify(self, string, phrases, parent=None):

		"""
		Stringifies phrases.

		After parsing of the string via self.parse(), this method takes the
		escaped string and the list of phrases returned by self.parse() and
		replaces the original phrases (with tags) with the Phrase-objects in
		the list and adds the appropriate flag-combinations as determined by
		the string or the position of the phrase (the string if it's in
		self.always, i.e. an 'always' argument). This method also works
		recursively to handle nested phrases (and resetting of parent-phrase
		styles).

		Arguments:
			string (str): The escaped string returned by self.parse().
			phrases (list): The list of Phrase-objects returned by self.parse().
			parent (Phrase): For recursive calls, the current parent Phrase.

		Returns:
			The finished, beautifully beautified string.

		Raises:
			errors.ArgumentError: If more positional arguments are requested
								  than were supplied.
		"""

		last_tag = 0

		beauty = ""

		for phrase in phrases:

			beauty += string[last_tag : phrase.opening]

			if phrase.arguments:
				combination = 0
				for n, i in enumerate(phrase.arguments):
					try:
						combination |= self.positional[i]
					except IndexError:
						raise errors.ArgumentError("Positional argument '{}' "
							 					   "(index {}) is out of"
							 					   "range!".format(i, n))

				# If override-mode is on (turned on by ! operator) the
				# positional arguments should override the 'always'-style
				if phrase.string in self.always and not phrase.override:
					combination |= self.always[phrase.string]

				phrase.style = flags.codify(combination)

			elif phrase.string in self.always:
				phrase.style = flags.codify(self.always[phrase.string])

			else:
				try:
					phrase.style = flags.codify(self.positional[self.counter])
					self.counter += 1
				except IndexError:
					requested = errors.number(self.counter + 1)
					available = len(self.positional)
					raise errors.ArgumentError("Requested {} formatting "
											   "argument for '{}' but only "
											   "were supplied {} were supplied"
											   "!".format(requested,
											   			  phrase.string,
											   			  available))
			if phrase.nested:
				phrase.string = self.stringify(phrase.string,
											   phrase.nested,
											   phrase)

			# After a nested phrase is over, we reset the style to the
			# parent style, this gives the notion of nested styles.
			reset = parent.style if parent else ""

			# \033[ signifies the start of a command-line escape-sequence
			beauty += "\033[{}m{}\033[0;{}m".format(phrase.style,
													phrase,
													reset)
			last_tag = phrase.closing + 1

		if last_tag < len(string):
			beauty += string[last_tag:]

		return beauty
