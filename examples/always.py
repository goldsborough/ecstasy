#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import ecstasy

def main():

	text = "<Muffins> <are> <super> <radical>!"

	styles = {
	    ("Muffins", "super"): ecstasy.Color.Blue,
	    "radical": ecstasy.Style.Blink
	}

	text = ecstasy.beautify(text, styles, are=ecstasy.Fill.Red)

	print(text)

if __name__ == "__main__":
	main()