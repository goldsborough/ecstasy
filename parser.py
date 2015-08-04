# -*- coding: utf-8 -*-

import re
import collections

from . import flags
from . import errors

class Phrase:
	def __init__(self,
				 string,
				 opening,
				 closing,
				 argument=None):

		self.string = string
		self.opening = opening
		self.closing = closing
		self.argument = argument
		self.style = None

class Parser:
	def __init__(self, args, kwargs):

		self.always = kwargs
		self.positional = self.handle_arguments(args)

	def handle_arguments(self, args):

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

		phrases = self.parse(string)

		if not phrases:
			return string

		return self.stringify(string, phrases)

	def parse(self, string):

		#<Hello <World> waffles>
		#<Hello <World <what> is> going <on> <with <you> today> girl!>
		#<1 \> 0>
		#<Hello>

		phrases = [ ]

		opening = string.find("<")

		tags = re.compile(r"[<>]")

		opened = 0

		while opening != -1:

			# Check for escaping
			if string[opening - 1] == "\\":
				opening = string.find("<", opening + 1)
				continue

			# Look for the substring closing tag (either the
			# closing tag of the argument or of the phrase)
			first = string.find(">", opening + 1)

			if first == -1:
				position = errors.position(string, opening)
				word = string[opening + 1:].split()[0]
				raise errors.ParseError("No closing tag found for opening tag " +
						 				"at position " + position + 
										"just before the word '{}'!".format(word))

			# Look for another < or > tag, if < tag found
			# next then first is really the closing
			# tag of a phrase, else if > found then first
			# is the end of the argument group (e.g. <0>...>),
			# after which second.start() is the real closing tag
			second = tags.search(string, first + 1)

			# Whatever is between the opening tag and the first 
			# closing tag. This can either be the phrase or the
			# positional argument
			substring = string[opening + 1 : first]

			# Normal mode, no positional argument
			if not second or second.group() == "<":
				phrases.append(Phrase(substring,
									  opening,
									  first))
				if second:
					# Since we already have it
					opening = second.start()
					continue
				break

			# Escaped mode -> normal mode
			elif substring[-1] == "\\":
				# Get rid of escape character
				phrase = substring[:-1] + string[first : second.start()]
				phrases.append(Phrase(phrase,
									  opening,
									  second.start()))

			# Argument mode, check for argument
			elif substring.isdigit():
				phrases.append(Phrase(string[first + 1 : second.start()],
							   		  opening,
							   		  second.start(),
							   		  int(substring)))

			else:
				position = errors.position(string, opening + 1)

				raise errors.ArgumentError("Argument '{}' at position {} is "
										   "neither a number nor the escape "
										   "character ('\\')"
										   "!".format(substring, position))

			# For escaped and argument mode
			opening = string.find("<", second.start() + 1)

		return phrases

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
