=======
Ecstasy
=======

Contents:

* Introduction
* Basic Usage
* Description
* Phrase Arguments
* Passing Flags
* Source Code

Introduction
============

Basic Usage
===========

Description
===========

Phrase Arguments
================

Ecstasy Flags
=============

How you can

Available flags

Source Code
===========

As you can see, a piece of text (a "phrase") is *marked* simply by putting it in <tags>. For each phrase, you must specify one style flag (or bitwise-OR'd combination thereof). Like for Python's built-in str.format() method, the order in which styles are mapped to phrases is sequential, i.e.  A phrase can also have a positional argument as in '<0>just>'. If ecstasy finds a positional argument, it will pick the style from its pool (the styles you passed to it) at that index, rather than incrementing its counter and chosing the next style.
