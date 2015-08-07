#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import ecstasy

def main():

	text = "<NaNaNa> <NaNaNa>\n<NaNaNa> <NaNaNa>\n<Batman>"

	line_1 = [ecstasy.Style.Blink, ecstasy.Color.Blue]
	line_2 = [ecstasy.Color.Yellow, ecstasy.Fill.Red]

	text = ecstasy.beautify(text, line_1, line_2, ecstasy.Style.Bold)

	print(text)

if __name__ == "__main__":
	main()