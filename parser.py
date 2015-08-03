#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import re

from . import flags

from .errors import ParseError, ArgumentError

class Phrase:
	def __init__(self, string, opening, closing, arg=None):
		self.string = string
		self.opening = opening
		self.closing = closing
		self.argument = arg

def beautify(string, formats, always):
	
	phrases = parse(string)

	if not phrases:
		return string

	# Expand the any tuples passed to
	# the 'always' keyword arguments
	for key, value in always.items():
		if type(key) == tuple:
			for i in key:
				always[i] = value

	counter = last = 0

	beauty = ""

	for phrase in phrases:

		beauty += string[last : phrase.opening]

		if phrase.argument is not None:
			try:
				codes = codify(formats[phrase.argument])
			except IndexError:
				raise ArgumentError("Out of range positional argument" 
								    " '{}'!".format(phrase.argument))
		elif phrase.string in always:
			codes = codify(always[phrase.string])
		else:
			try:
				codes = codify(formats[counter])
				counter += 1
			except IndexError:
				raise ArgumentError("At least {} formatting arguments "
							        "required but {} were supplied"
									"!".format(counter + 1, len(formats)))

		beauty += "\033[{}m{}\033[0m".format(codes, phrase.string)

		last = phrase.closing + 1

	if last < len(string):
		beauty += string[last:]

	return beauty

def parse(string):

	phrases = [ ]

	opening = string.find("<")

	tags = re.compile(r"[<>]")

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
			raise ParseError("No closing tag found for opening tag " +
			 				 "at position" + position + 
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
			raise ArgumentError("Argument '{}' at position {} "
								"is neither a number nor the escape "
								"character!".format(substring, position))

		# For escaped and argument mode
		opening = string.find("<", second.start() + 1)

	return phrases

def codify(combination):

	codes = []

	for enum in (flags.Format, flags.Color, flags.Fill):
		for flag in enum:
			if combination & flag:
				codes.append(str(flag))
				
	return ";".join(codes)
