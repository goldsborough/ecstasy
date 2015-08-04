# -*- coding: utf-8 -*-

import re
import warnings
import collections

from . import flags
from . import errors

class Phrase:
	def __init__(self,
				 opening=None,
				 closing=None,
				 string=None,
				 argument=None,
				 style=None):

		self.string = string

		self.opening = opening
		self.closing = closing

		self.argument = argument

		self.style = style

		self.nested = []

	def __str__(self):
		return self.string

class Parser:
	def __init__(self, args, kwargs):

		self.always = kwargs

		self.positional = self.process_flags(args)

		self.tags = re.compile(r"[<>]")

	def process_flags(self, args):

		positional = []

		for argument in args:
			# A flag is an instance of a subclass of
			# flags.MetaEnum if it was passed alone
			if isinstance(argument, flags.MetaEnum):
				positional.append(argument)

			# or is an integer if it was (bitwise) OR'd
			# with another flag (a "flag combination")
			elif isinstance(argument, int):
				if argument < 0 or argument >= flags.limit:
					raise EcstasySyntaxError("Flag value '{}' is out of range "
											 "!".format(argument))
				positional.append(argument)

			# Dictionaries store 'always'-arguments
			elif isinstance(argument, dict):
				for key, value in argument.items():
					# Simple 'always'-argument where one string
					# is mapped to one formatting flag-combination
					if type(key) == str:
						self.always[key] = value

					# Complex 'always'-argument with a
					# tuple containing strings, each with the same
					# flag-combination (same value)
					elif type(key) == tuple:
						for i in key:
							self.always[i] = value
					else:
						raise TypeError("Key '{}' in dictionary "
										"argument passed at index {} "
										"is neither a string nor a tuple "
										"of strings!".format(key, n))

			elif isinstance(argument, collections.Iterable):
				for element in argument:
					try:
						element = int(element)
					except TypeError:
						raise TypeError("Element {} is neither a flag nor a "
										"(bitwise) OR'd flag-combination"
										"!".format(element))

					if element < 0 or element >= flags.limit:
						raise EcstasySyntaxError("Flag value '{}' is out of range "
												 "!".format(element))
					positional.append(element)
			else:
				raise TypeError("Argument '{}' is neither a flag, a (bitwise) "
								"OR'd flag-combination, a dictionary or an "
								"iterable of positional arguments"
								"!".format(argument))

		return positional

	def beautify(self, string):

		string, phrases = self.parse(string)

		if not phrases:
			return string

		s = lambda p: "{}, {{{}}}, [{}]".format(p.string, p.argument, len(p.nested))

		f = lambda p, d=1: s(p) + "\n" + "\t"*d + ("\n" + "\t" * d).join(f(i,d+1) for i in p.nested) if p.nested else s(p)

		print("")

		for i in phrases:
			print(f(i))

		print("")

		print(string)

		#return self.stringify(string, phrases)

	def parse(self, string, phrase=None):

		# When phrase is None (at the first call)
		# we return a list of phrase, else this 
		# function will return a phrase object
		# this is because there is no 'root' phrase
		if phrase:
			tag = self.tags.search(string, phrase.opening + 1)
		else:
			phrases = []
			tag = self.tags.search(string)

		while tag:
			if tag.group() == "<":
				opening = tag.start()

				print("Opening tag ('<') at position {}".format(opening))

				# Check for escaping
				if string[opening - 1] == "\\":
					# Remove the escape character
					string = string[:opening - 1] + string[opening:]

					# When removing the escape character, the
					# opening tag index is pushed one back
					opening -= 1

					# If the escape character was not itself (double)
					# escaped we can look for the next tag
					if opening == 0 or string[opening - 1] != "\\":

						print("Escaped opening tag at "
							  "position {}".format(tag.start()))

						tag = self.tags.search(string, tag.start())
						continue

				# Initialize the Phrase passed on with its opening
				# tag position. It is then returned with all attributes
				# set and possibly with more nested phrases
				child = Phrase(opening)
				string, child = self.parse(string, child)

				if phrase:
					phrase.nested.append(child)
				else:
					phrases.append(child)

				tag = self.tags.search(string, child.closing + 1)

			# tag is closing ('>')
			elif phrase:

				print("Closing tag ('>') at position "
							  "{}".format(tag.start()))

				# Whatever is between the opening tag and this closing tag
				substring = string[phrase.opening + 1 : tag.start()]

				print("Substring " + substring)

				# Positional argument <x>
				if substring.isdigit():

					print("Found positional argument '{}' at position "
						  "{}".format(substring, phrase.opening + 1))

					phrase.argument = int(substring)

					tag = self.tags.search(string, tag.end())

				# Escape-character to escape the closing tag (/>)
				elif substring.endswith("\\"):

					# Get rid of the escape character either way
					string = string[:tag.start() - 1] + string[tag.start():]

					# Double-escape means this is really supposed to be a
					# closing tag and thus we can return the phrase.
					if substring[:-1].endswith("\\"):

						# Offset because we removed the escape character
						phrase.closing = tag.start() - 1

						phrase.string = string[phrase.opening + 1 : phrase.closing]

						return string, phrase

					# tag.start() is now one index passed the closing tag
					tag = self.tags.search(string, tag.start())

				else:
					phrase.closing = tag.start()

					if phrase.argument is None:
						phrase.string = substring
					else:
						# The substring should not include the argument
						phrase.string = substring[substring.find(">") + 1:]

					print("New phrase '{}'".format(phrase))

					return string, phrase

			else:
				# Replace escape character
				if tag.start() > 0 and string[tag.start() - 1] == "\\":
					string = string[:tag.start() - 1] + string[tag.start():]
				else:
					# When the phrase is None at the start, there should not
					# be a closing tag because none was ever opened. This is
					# not actually an error, but we should warn about it.
					position = errors.position(string, tag.start())
					warnings.warn("Un-escaped '>' character at "
							 	  "position {}".format(position),
								  Warning)

				tag = self.tags.search(string, tag.end())

		if not phrase:
			return string, phrases

		# If this is not the first stack-depth the function should
		# have returned upon finding a non-argument closing tag,
		# i.e. we should never have gotten here.
		position = errors.position(string, phrase.opening)
		word = re.search(r"([\w\s]+)(?![\d]*>[\w\s]+>)",
					    string[phrase.opening + 1:])

		raise errors.ParseError("No closing tag found for opening tag "
								"at position {}, right after '{}'"
								"!".format(position, word.group()))

	def stringify(self, string, phrases, parent=None):

		counter = last = 0

		beauty = ""

		for phrase in phrases:

			beauty += string[last : phrase.opening]

			if phrase.argument is not None:
				try:
					codes = self.codify(self.positional[phrase.argument])
				except IndexError:
					raise errors.ArgumentError("Out of range positional "
											   "argument '{}'"
											   "!".format(phrase.argument))
			elif phrase.string in self.always:
				codes = self.codify(self.always[phrase.string])
			else:
				try:
					codes = self.codify(self.positional[counter])
					counter += 1
				except IndexError:
					raise errors.ArgumentError("At least {} formatting "
											   "arguments required but {} "
											   "were supplied"
											   "!".format(counter + 1,
											   			  len(positional)))

			beauty += "\033[{}m{}\033[0m".format(codes, phrase.string)

			last = phrase.closing + 1

		if last < len(string):
			beauty += string[last:]

		return beauty

	def codify(self, combination):

		codes = []

		for enum in (flags.Format, flags.Color, flags.Fill):
			for flag in enum:
				if combination & flag:
					codes.append(str(flag))

		return ";".join(codes)
