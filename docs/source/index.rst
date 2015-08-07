=======
Ecstasy
=======

\

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

::

    import ecstasy

    text = "<Cats> are <(0)just> <<small>, furry <elephants>>!"

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

Ecstasy works on *phrases*. A phrase is a marked up region of text inside a string that fits the following schema:

::

     <[(x[,y,z,...][![,+]])]...>

Here, the second ellipsis (...) represents any character sequence that is eventually beautified by ecstasy. This character sequence *must* be placed between exactly one opening tag and one closing tag (as in HTML). The sequence in parantheses is the optional set of *arguments* of the phrase. In the simplest case, this set of arguments is only one single positional argument -- i.e., a digit -- specifying the index of the style to pick for this phrase (the index referring to the pool of styles passed to ecstasy.beautify()).

.. note::

    Precede a tag with a backslash ("\\") to prevent ecstasy from intepreting it as a meta-character. "<a>" will result in the parsing of one phrase with the string "a", but "\\<a\\>" will cause no phrase to be parsed (escaping the closing tag is not strictly necessary, but not doing so will produce a warning).

Categories
----------

The above paragraph introduces two of the three categories of *phrases* known to ecstasy:

* **Simple phrases**, following the schema <...> (w/o arguments). Whenever ecstasy encounters a simple phrase, it will pick the next available style in its pool of flag-combinations (those supplied via beautify()) and increment an internal counter, such that following simple phrases will be mapped to following styles. As an example, given the string "<a> <b>", containing two simple phrases, and the list of styles (discussed in further detail below) [ecstasy.Color.Red, ecstasy.Style.Blink], the phrase "<a>" will be parsed first and mapped to the first available style (ecstasy.Color.Red). The internal counter is then incremented so that when the next phrase "<b>" is parsed, it will map to the *next available style*, in this case ecstasy.Style.Blink.

\

* **Argument phrases**, following the schema <(x[,y,z,...][![,+]])>...>. An argument phrase differs from a simple phrase in that it is additionally supplied with one or more arguments in parantheses. The topic of arguments is discussed in further detail below, but in the most obvious and simple case there is only one single argument -- an index ---, referred to as a *positional argument*, which tells ecstasy to not pick the next available style and increment the counter as it would for a simple phrase, but rather simply pick the style at the index specified by the positional argument, without incrementing. Now, given the string "<a> <(0)b>" and *only one style*, "<a>" will be parsed as a simple phrase and consume the next available style (the only one). However, when "<(0)b>" is parsed, the style assigned to it will be that at index 0, i.e. the same one as for "<a>".

There is one more important phrase-category which can be seen in the basic-usage example given at the top of this document:

* **Always phrases**, following the full schema <[x[,y,z,...][![,+]]>]...>. An *always* phrase is essentially a keyword-argument consisting of a key -- some specific string -- and an associated value -- a certain style (flag-combination) that is passed to ecstasy.beautify() via the standard Python keyword argument syntax, i.e. key=value or, more specifically here, string=style. Whenever ecstasy encounters a phrase (<...>) in the string it is parsing, containing exactly that string specified by the *always*-argument, that phrase will *always* be assigned the style of the *always*-argument rather than any from the pool of styles from which simple or argument phrases retrieve their formatting. In the basic-usage example, "<small>" is an *always* phrase because the user notified ecstasy that it should always pick the associated style when it encounters the string "small" (i.e. the phrase "<small>"), by explicitly passing small=ecstasy.Style.Invert | ecstasy.Color.White to ecstasy.beautify() using the keyword syntax. There are ways to override this '*always*' behaviour, explained in the section on arguments.

Nesting
-------

It is important to mention that phrases (and any type thereof) can be nested. Nested styles cascade, i.e. in a nested phrase, all children phrases assume the style of the parent phrase unless a categorically-equivalent flag is supplied to a child phrase that overrides the parent flag in that category. Take, for example, the string "<a <b> c <d>>". First of all, here, three styles must be supplied to ecstasy.beautify() as the internal counter does not consider nesting in any way (one simple phrase = one extra style). If the first style (index 0 in the pool), that of the outermost phrase (<a ...>) includes the color red (ecstasy.Color.Red), then by default everything inside this phrase will be colored red, i.e. the characters 'a', 'b', 'c' and 'd'. If, now, b's style (at index 1 in the pool) contains the blinking command (ecstasy.Style.Blink), b will blink in red. The character 'c', however, will only be red again (the style is reset to the parent style after a nested phrase has been parsed). At the same time, if the flag combination at index 2 in the pool contains ecstasy.Color.Blue, this will override the categorically-equivalent parent flag ecstasy.Color.Red (because both are from the ecstasy.Color enum). 

Arguments
=========

This section discusses the two types of arguments that you can supply to a phrase: positional arguments and modifiers. In general, all arguments of a phrase must be placed *inside parantheses* at the *start* of the phrase. If there is any space or other character(s) between the opening tag of the phrase and the opening paranthesis of the argument sequence, ecstasy will not interpret the arguments as arguments, but will instead warn about un-escaped meta-characters. 

.. topic:: Escaping

    To have a literal set of parantheses inside a phrase that should not denote an argument sequence, you should precede *both* paranthesis characters with backslashes ("\\"). Note that, as explained above, any character between the opening tag and the opening paranthesis will cause the arguments not to be interpreted as arguments, but only the escape-character will actually be removed by ecstasy, i.e. the escape character is the only way to get the verbatim parantheses *right* after the opening tag without them being interpreted as arguments. 

Positional Arguments
--------------------

When a (numeric) positional argument is supplied to a phrase, ecstasy will assign it the style found in the pool of styles at the index denoted by the positional argument. The internal counter that determines which style is picked next for simple phrases is not incremented.

::

    text = "<Hello> <(0)World> <!>"

    text = ecstasy.beautify(text,
                            ecstasy.Color.Red,
                            ecstasy.Fill.Blue)

Here, "<Hello>" will first be parsed as a simple phrase. The internal counter will be zero initially, and as such the style at index zero is picked for this phrase. The counter is then incremented to 1. The next phrase "<(0)World>"  is parsed as an *argument-phrase* and has the single positional argument '0'. Because it is an argument phrase, its style is determined from its argument and this is, here, the style at index 0 (the same one as before). The counter is not incremented and stays at 1. The next phrase "<!>" is again a simple phrase and will pick the style at the index of the counter. In the output string, "Hello" and "World" are colored Red, while the exclamation mark is given a blue fill. 

.. note::

    Negative indices are allowed and follow the same meaning as in regular Python (as in -1 being the last element).

.. note::

    If the positional argument is out of range (i.e. if the index is greater than or equals the size of the pool), an exception of type ecstasy.errors.ArgumentError is thrown.

Multiple Positional Arguments
*****************************

It is possible to specify more than one positional argument, separated from one another by a comma (whitespace allowed). In such a case, the styles at the individual indices in the pool, specified by the positional arguments, are simply combined.

**Example:**::

    text = "<(0, 1)Llamas>"

    text = ecstasy.beautify(text,
                            ecstasy.Color.Green,
                            ecstasy.Style.Blink)

In this case, there are multiple positional arguments for the phrase "Llama". They are combined (as if it had been done manually via bitwise-OR) and the resulting string has a green color and also blinks.

Modifiers
---------

When ecstasy finds a phrase that matches one of its *always*-phrases, it will, normally, pick the style associated with the always argument and assign it to the phrase. Ecstasy allows alterations to this standard behaviour with the modifier operators '!' and '+'. The types of alterations depend on the phrase category. When and why is this useful? Mainly when you have multiple phrases matching a certain *always*-argument and you want most of them styled uniformly, but you would like to make an exception for one or a few of these phrases (exempt them from the *always* rule).

Simple Phrase Modifiers
***********************

First, the default behaviour for always-phrases:

::

    text = "<Unicorn> <mushrooms>"

    text = ecstasy.beautify(text,
                            ecstasy.Style.Underline,
                            Unicorn=ecstasy.Style.Bold)

"Unicorn" will be bold and "mushrooms" is underlined.

For simple phrases, the '+'-operator (the *increment*-operator) causes the phrase to not only be styled with the flag-combination specified by the always argument, but will additionally **combine** it with the style at the current counter index and then increment the counter.

::

    text = "<(+)Unicorn> <mushrooms>"

    text = ecstasy.beautify(text,
                            ecstasy.Style.Underline,
                            ecstasy.Color.Yellow,
                            Unicorn=ecstasy.Style.Bold)

In this case, "Unicorn" will receive its *always*-style, but this style will be *combined* with the style at the current counter index (zero initially). As such, "Unicorn" will be bold and underlined. The counter is then incremented, thus "mushrooms" will appear yellow.

If, additionally, the '!'-operator (the *override*-operator) is supplied, the style at the current counter index overrides the style from the always-argument, rather than them being combined.

::

    text = "<(!+)Unicorn> <mushrooms>"

    text = ecstasy.beautify(text,
                            ecstasy.Style.Underline,
                            ecstasy.Color.Yellow,
                            Unicorn=ecstasy.Style.Bold)

Here, "Unicorn" will completely override its *always*-style and will just be underlined (the *always*-style is ignored). "mushrooms" is still yellow.

.. note:: The order of operators is not important: (!+) is the same (+!).

If the '!'-operator is supplied alone (without the '+'-operator), this will produce only the overriding-behaviour, but will not increment the counter.

::

    text = "<(!)Unicorn> <mushrooms>"

    text = ecstasy.beautify(text,
                            ecstasy.Style.Underline,
                            ecstasy.Color.Yellow,
                            Unicorn=ecstasy.Style.Bold)

    print(text)

Now, the "Unicorn" phrase will again override its *always*-style, but will not increment the internal counter (the *increment*-operator is missing). Therefore, "Unicorn" will be underlined, and the same goes for "mushrooms", because the counter is still zero when it is reached. The second style in the pool, ecstasy.Color.Yellow, is never used, nor is the *always*-argument. 

.. note::

    If you want to combine the always-argument's style with the style at the current counter index, without incrementing, use a positional argument (those combine with always-arguments default).

Positional Phrase Modifiers
***************************

By default, when a positional-phrase is also an *always*-phrase, the *always*-style will cascade (is combined) with the style(s) of the phrase(s) at the specified position(s) in the pool:

::

    text = "<(0,1)Batman>"

    text = ecstasy.beautify(text,
                            ecstasy.Fill.White,
                            ecstasy.Style.Dim,
                            Batman=ecstasy.Color.Black)

In this situation, the *always*-style (black text-color) is combined with the style at index 0 and 1 in the pool. "Batman" will appear with a white background, a black text color and is dimmed-down.

For positional phrases, there is only the override operator to change this default behaviour: '!'. The override operator will cause the positional phrase to ignore its *always*-style and just pick the style(s) at its positional index/indices:

::

    text = "<(0,1!)Batman>"

    text = ecstasy.beautify(text,
                            ecstasy.Fill.White,
                            ecstasy.Style.Dim,
                            Batman=ecstasy.Color.Black)

Here, the positional-styles entirely override the *always*-style and "Batman" has a white background and is dimmed-down, but no longer has a black text-color.

.. note::

    Arguments, both modifiers and positional, are well-formed if they match the following regular expression:

    ::

    ^(-?\d,?)+!?$|^!?(-?\d,?)+$|^(!\+?|\+!?)$

Flags
=====

There are (currently) 41 style, text color and fill color flags that you can supply to ecstasy to beautify your strings. You may access style flags via the ecstasy.Style enum (brought to package-level from the ecstasy.flags module), the color flags via the ecstasy.Color enum and the fill flags you can find in ecstasy.Fill. Note that while you can specify as many (unique) style flags as you want, color and fill flags will override each other, i.e. the one with the highest position in the respective enum will override previous flags --- you can only have exactly *one* text color and exactly *one* fill color, so just never supply more than one.

Available Flags
---------------

\

* Style (ecstasy.Style)

    #. Reset: Resets all formatting (useful for nested phrases).
    #. Bold: Makes text appear in bold letters (strong emphasis).
    #. Dim: Dims-down text (appears darker).
    #. Underline: Underlines text.
    #. Blink: Makes text blink (1 Hertz).
    #. Invert: Swaps the fill and text colors.
    #. Hidden: Hides text (useful for passwords).


* Text Color (ecstasy.Color)

    #. Default (your terminal's default text color)
    #. Black
    #. DarkRed
    #. DarkGreen
    #. DarkYellow
    #. DarkBlue
    #. DarkMagenta
    #. DarkCyan
    #. Gray
    #. DarkGray
    #. Red
    #. Green
    #. Yellow
    #. Blue
    #. Magenta
    #. Cyan
    #. White

Here the output, ordered as above:

.. image:: https://github.com/petergoldsborough/ecstasy/docs/img/color.png
    :alt: illuminati was here

* Fill Color (ecstasy.Fill)

    #. Default (your terminal's default background)
    #. Black
    #. DarkRed
    #. DarkGreen
    #. DarkYellow
    #. DarkBlue
    #. DarkMagenta
    #. DarkCyan
    #. Gray
    #. DarkGray
    #. Red
    #. Green
    #. Yellow
    #. Blue
    #. Magenta
    #. Cyan
    #. White

Here the output, ordered as above:

.. image:: https://github.com/petergoldsborough/ecstasy/docs/img/fill.png
    :alt: illuminati was here

Passing Flags
-------------

There are two ways to pass flags to ecstasy. The first method has been shown in this document all along: individually passing positional and keyword arguments to ecstasy.beautify:

::

    text = ecstasy.beautify(text,
                            ecstasy.Style.Blink,
                            borat=ecstasy.Style.Reset)


"But for my command-line tool, I may have dozens of flags, organized in lists. Am I to pass them all to this method individually? Ain't nobody got time fo dat!" I feel you! Fortunately, it is equally possible to pass flags not individually like above, but to pass them in *one or more* iterables. This way, you can more easily organize the many flags you may have and more easily interchange individual flags within that list. For example, one could pass one list per paragraph or section. This is for your convenience only, as lists are simply expanded, no matter how deeply nested they are (recursion <3), such that passing a list is equivalent to passing each flag individually. You can also mix lists with individual arguments:

::

    text = "<NaNaNa> <NaNaNa>\n<NaNaNa> <NaNaNa>\n<Batman>"

    line_1 = [ecstasy.Style.Blink, ecstasy.Color.Blue]
    line_2 = [ecstasy.Color.Yellow, ecstasy.Fill.Red]

    text = ecstasy.beautify(text, line_1, line_2, ecstasy.Style.Bold)

The same goes for keyword (*always*) arguments and dictionaries:

::

    text = "<Muffins> <are> <radical>!"

    styles = {
        "Muffins": ecstasy.Color.Blue,
        "radical": ecstasy.Style.Blink
    }

    text = ecstasy.beautify(text, styles, are=ecstasy.Fill.Red)

However, there are actually two major benefits of passing an *always*-argument in a dictionary rather than individually to the ecstasy.beautify(). First of all, rather than having to specify each style for each *always*-argument even if they are all the same, with a dictionary, it is possible to have not one single string as a key, but a tuple of strings which is then expanded. Each string in a tuple will have the same style:

::

    text = "<Muffins> <are> <radical>!"

    styles = {
        ("Muffins", "are"): ecstasy.Color.Blue,
        "radical": ecstasy.Style.Blink
    }

    text = ecstasy.beautify(text, styles)


The second big advantage dictionaries have over individual keyword-arguments is that they are not subject to naming restrictions. On the one hand, this includes the fact that keyword-arguments (due to Python's syntax rules) cannot have spaces in them, while a string in a dictionary can. On the other hand, this also means that you can use restricted Python keywords such as *if*, *is*, *for*, *return* etc. for your *always*-arguments. This is normally not possible with keyword-arguments.

::

    text = "<return> <my space ship> <if> "\
           "grandmother ever <import>s "\
           "Kentucky Fried Whale"


    # Invalid. All of it. ALL OF IT!!!!!!!
    #text = ecstasy.beautify(text,
    #                        return=ecstasy.Color.Blue,
    #                        my space ship=ecstasy.Style.Blink,
    #                        if=ecstasy.Color.Blue,
    #                        import=ecstasy.Fill.Yellow)

    styles = {
        ("return", "if"): ecstasy.Color.Blue,
        "my space ship": ecstasy.Style.Blink,
        "import": ecstasy.Fill.Yellow
    }

    # Legal AF
    text = ecstasy.beautify(text, styles)


Source Code
===========

.. toctree::
    :maxdepth: 2

    modules.rst
