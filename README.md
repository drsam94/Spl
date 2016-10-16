SPL
===

Shakespeare Compiler written in Python, splc.py

This is a compiler from SPL to C that implements the majority of the Shakespeare programming
language invented by Kalle Hasselstrom and Jon Aslund, I take no credit for inventing the language.

This software is free to edit, use, or sell, but I wouldn't mind if you attached the following
copyright notice to any work that utilizes this project.

    Copyright © 2014-2015 Sam Donow 
    sad3@williams.edu
    drsam94@gmail.com

This compiler implements most features of the Shakespeare Programming language described at
http://shakespearelang.sourceforge.net/report/shakespeare/

The following features have yet to be or may never be implemented:

- Stacks (because who needs data structures in Shakespeare, really?)
- multiple-word nouns in cases where using just the last word would generate any confusion

The following features not in the original language spec is implemented but is a work in progress:

### Pretty Gotos

In the original language spec, goto statements take the form `let us proceed to scene III`, `let us return to act I`,
etc. As this is both awkward and non-Shakesperian, I have made it so that you can use the name of an act or scene (not case,
punctuation, or whitespace sensitive) in place of a this awkward structure. Therefore, if you had
`Act I: The Forest`.

Then the sentence `let us return to the forest` is equivalent to `let us return to act I`.

Like standard gotos, you can not jump to a scene within an act other than the one you are currently in.

### Initial Declarations

In the original language, everything after the comma in a declaration, such as:

    Romeo, an evil octopus.

is ignored: so in the above, though octopus is not a Shakespearean noun, this is allowed. However, the spec does not make it clear what the initial value of a variable should be, which would lead to undefined behavior. In SPL, you can put a noun phrase after Romeo, and it will be evaluated to a number, so for example

    Romeo, a good man.

will assign 2 to Romeo. Any non-legal noun phrase will assign 0 instead (as though it had been ignored).

----------

The following are planned features not in the original language spec that may be implemented in
later versions of this compiler.

- Support for word replaces of functions: If the goal of Shakespeare is to make programs look like plays, then it is sub-optimal having to use words like "square root" all over the place, so I may add a way to define equivalent words for math functions in a text file.

To use spl, simply run

    $ ./spl [Input File]
    $ ./a.out

Or, if you would like, you can run

    $ python splc.py [Input File] > [Output File]
    $ gcc [Output File] -lm
    $ ./a.out

The spl script should work in any bash terminal, on Windows, the explicit python method should work if you have
all of the right programs installed. I may at some time get around to writing a .bat script for Windows users.

Depenencies:
- Python (2.X or 3.X)
- gcc
