Description
===========

nested,
keyword

Ecstasy works on *phrases*. A phrase is a marked up region of text inside a string that fits the following schema:::

	 <[x[,y,z,...][!]>]...>

Here, the dots (...) represent any character sequence that is eventually beautified by ecstasy. This character sequence *must* be placed between exactly one opening tag and one closing tag (as in HTML). The sequence in brackets (<**[x[,y,z,...][!]>]**...>) is the optional set of *arguments* of the phrase. In the simplest case, this set of arguments is only one single positional argument -- i.e., a digit -- specifying the index of the style to pick for this phrase (the index referring to the pool of styles passed to ecstasy.beautify()). This introduces two of the three categories of *phrases* known to ecstasy:

* **Simple phrases**, following the schema <...> (w/o arguments). Whenever ecstasy encounters a simple phrase, it will pick the next available style in its pool of flag-combinations (those supplied via beautify()) and increment an internal counter, such that following simple phrases will be mapped to following styles. As an example, given the string "<a> <b>", containing two simple phrases, and the list of styles (discussed in further detail below) [ecstasy.Color.Red, ecstasy.Style.Blink], supplied by the client, the phrase "<a>" will be parsed first and mapped to the first available style (ecstasy.Color.Red). The internal counter is then incremented so that when the next phrase "<b>" is parsed, it will map to the *next available style*, in this case ecstasy.Style.Blink.

* **Argument phrases**, following the schema <x[,y,z,...][!]>...>. An argument phrase differs from a simple phrase in that it is additionally supplied with an argument (duh). What is allowed as an argument is described with greater care further below, but what is important to note here is that an argument is always