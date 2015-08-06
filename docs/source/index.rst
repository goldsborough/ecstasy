=======
Ecstasy
=======

Contents:

* `Introduction`_
* `Basic Usage`_
* `Phrases`_
* `Arguments`_
* `Flags`_
* `Source Code`_

Introduction
============

Ecstasy is a Python package and markup language that makes your command-line tool so much more beautiful and pretty. It works by parsing a specially marked-up string and inserting command-line-specific escape-sequences that alter the strings appearance by giving it pretty colors, underlining it, making it blink, turning it bold or dim or even hiding it. When printed to a command-line, these escape-sequences are then interpreted appropriately and the originally hideous string is suddenly all marvelous and pretty.

Basic Usage
===========

To use ecstasy, you mark up a standard Python string using ecstasy's special syntax, chose some sassy styling and formatting flags, pass them on to the package-level beautify() method and, in return, get your beautified string, ready to kick ass when printed to your command-line:

.. code-block:: python

    import ecstasy

    text = "<Cats> are <0>just> <<small>, furry <elephants>>!"

    text = ecstasy.beautify(text,
                            ecstasy.Style.Blink | ecstasy.Color.Red,
                            ecstasy.Style.Bold | ecstasy.Fill.Blue,
                            ecstasy.Color.Magenta | ecstasy.Style.Underline,
                            small=ecstasy.Style.Invert | ecstasy.Color.White)

    print(text)

Running this in a script from a command-line outputs:

.. image:: https://github.com/goldsborough/ecstasy/docs/img/usage.gif
    :alt: Badassery

Phrases
=======

Ecstasy works on *phrases*. A phrase is a marked up region of text inside a string that fits the following schema:::

     <[x[,y,z,...][![,+]]>]...>

Here, the second ellipsis (...) represents any character sequence that is eventually beautified by ecstasy. This character sequence *must* be placed between exactly one opening tag and one closing tag (as in HTML). The sequence in brackets (<**[x[,y,z,...][!]>]**...>) is the optional set of *arguments* of the phrase. In the simplest case, this set of arguments is only one single positional argument -- i.e., a digit -- specifying the index of the style to pick for this phrase (the index referring to the pool of styles passed to ecstasy.beautify()). 

Categories
----------

The above paragraph introduces two of the three categories of *phrases* known to ecstasy:

* **Simple phrases**, following the schema <...> (w/o arguments). Whenever ecstasy encounters a simple phrase, it will pick the next available style in its pool of flag-combinations (those supplied via beautify()) and increment an internal counter, such that following simple phrases will be mapped to following styles. As an example, given the string "<a> <b>", containing two simple phrases, and the list of styles (discussed in further detail below) [ecstasy.Color.Red, ecstasy.Style.Blink], supplied by the client, the phrase "<a>" will be parsed first and mapped to the first available style (ecstasy.Color.Red). The internal counter is then incremented so that when the next phrase "<b>" is parsed, it will map to the *next available style*, in this case ecstasy.Style.Blink.

* **Argument phrases**, following the schema <x[,y,z,...][!]>...>. An argument phrase differs from a simple phrase in that it is additionally supplied with one or more arguments. The topic of arguments is discussed in further detail below, but in the most obvious and simple case there is only single argument -- an index ---, referred to as a *positional argument*, which tells ecstasy to not pick the next available style and increment the counter as it would for a simple phrase, but rather simply pick the style at that index without incrementing. Now, given the string "<a> <0>b>" and *only one style*, "<a>" will be parsed as a simple phrase and consume the next available style (the only one). However, when "<0>b>" is parsed, the style assigned to it will be that at index 0, i.e. the same one as for "<a>".

There is one more important and equally interesting phrase-category which can be seen in the basic-usage example given at the top of this document:

* **Always phrases**, following the full schema <[x[,y,z,...][![,+]]>]...>. An *always* phrase is essentially a keyword-argument consisting of a key -- some specific string -- and an associated value -- a certain style (flag-combination) that is passed to ecstasy.beautify() via the standard Python keyword argument syntax, i.e. key=value or, more specifically here, string=style. Whenever ecstasy encounters a phrase (<...>) in the string it is parsing, containing exactly that string specified by the *always*-argument, that phrase will *always* be given the style of the *always*-argument rather than any from the pool of styles from which simple or argument phrases retrieve their formatting. In the basic-usage example, "<small>" is an *always* phrase because the user notified ecstasy that it should always pick the associated style when it encounters the string "small" (i.e. the phrase "<small>"), by explicitly passing small=ecstasy.Style.Invert | ecstasy.Color.White to ecstasy.beautify() using the keyword syntax. There are ways to override this '*always*' behaviour, explained in the section on arguments.

Nesting
-------

Lastly, it is important to mention that phrases (and any type thereof) can be nested. Nested styles cascade, i.e. in a nested phrase, all children phrases assume the style of the parent phrase unless a categorically-equivalent flag is supplied to a child phrase that overrides the parent flag in that category. Take, for example, the string "<a <b> c <d>>". First of all, here, four styles must be supplied to ecstasy.beautify() as the internal counter does not consider nesting in any way (one simple phrase = one extra style). If the first style (index 0 in the pool), that of the outermost phrase (<a ...>) includes the color red (ecstasy.Color.Red), then by default everything inside this phrase will be colored red, i.e. the characters 'a', 'b', 'c' and 'd'. If, now, b's style (at index 1 in the pool) contains the blinking command (ecstasy.Style.Blink), b will blink in red. The character 'c', however, will only be red again (the style is reset to the parent style after a nested phrase has been parsed). At the same time, if the flag combination at index 2 in the pool contains ecstasy.Color.Blue, this will override the categorically-equivalent parent flag ecstasy.Color.Red (because both are from the ecstasy.Color enum). 

Arguments
=========

This section discusses the two types of arguments that you can supply to a phrase: positional arguments (<**[x[,y,z,...]**[![,+]]>]...>) and operator arguments (<[x[,y,z,...]**[![,+]]**>]...>). Generally, all arguments to a phrase must appear after the opening tag of the phrase. To signify the end of the sequence of arguments and the start of the actual phrase, another closing must be inserted. For the case that you wish to insert a literal closing tag/bracket character ('>') and not actually signify the end of an argument sequence, you can escape it by prepending a backward-slash character (\\>) -- i.e., <2 > 1> will mark 2 as a positional argument (space is ignored) and "1" as the phrase's string, while <2 \\> 1> will cause the phrase to have no arguments and its string to be "2 > 1".

Positional Arguments
--------------------

When a (numeric) positional argument is supplied to a phrase, ecstasy will assign it the style found in the pool of styles at the index denoted by the positional argument. The internal counter that determines which style is picked next for simple phrases is not incremented. 

If the positional argument is out of range (i.e. if the index is greater than or equals the size of the pool), an exception of type ecstasy.errors.ArgumentError is thrown. 

Flags
=====

asdfads

Available Flags
---------------

asdfads

Passing Flags
-------------

asdgs

Source Code
===========

.. toctree::
    :maxdepth: 2

    modules.rst
