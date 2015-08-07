# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import unittest

import ecstasy.flags as flags
import ecstasy.errors as errors

class TestCodify(unittest.TestCase):

	def test_codifies_single_flag(self):

		self.assertEqual(flags.codify(flags.Style.Reset),
						 str(flags.Style.Reset))

		self.assertEqual(flags.codify(flags.Style.Blink),
						 str(flags.Style.Blink))

		self.assertEqual(flags.codify(flags.Color.Red),
						 str(flags.Color.Red))

		self.assertEqual(flags.codify(flags.Fill.White),
						 str(flags.Fill.White))

	def test_codifies_flag_combination(self):

		combination = flags.Style.Underline | flags.Style.Blink

		expected = "{};{}".format(flags.Style.Underline,
				 				  flags.Style.Blink)

		self.assertEqual(flags.codify(combination), expected)

		combination = flags.Color.Red | flags.Fill.Black

		expected = "{};{}".format(flags.Color.Red,
								  flags.Fill.Black)

		self.assertEqual(flags.codify(combination), expected)

	def test_recognizes_bad_combination(self):

		self.assertRaises(errors.FlagError,
						  flags.codify,
						  -1)

		self.assertRaises(errors.FlagError,
						  flags.codify,
						  flags.LIMIT)

		self.assertRaises(errors.FlagError,
				  flags.codify,
				  flags.LIMIT + 100)

def main():
	unittest.main()

if __name__ == "__main__":
	main()
