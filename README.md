# PYBF

This is a pure-Python implementation of a Brainfuck interpreter, debugger, 
and several other utilities.  It runs on an infinite-length tape, with cells
extending as far as needed in both directions (left and right).  By default,
cells wrap around at 256, however this can be changed.

For those unfamiliar with Brainfuck, run.  You can still find Jesus.
Or [come to the dark side](https://en.wikipedia.org/wiki/Brainfuck).

## Tools

This package includes a Brainfuck interpreter, debugger, and several
translators (some of them optimizing).

### Interpreter

The main interpreter is in the `pybf.py` file.  It handles the actual
execution of the code, with the debugger heavily integrated.  It supports
both RAM-access and disk-accessed tape storage, adjustable cell wraparound
sizes, and (theoretically) re-mappable commands.

### Debugger

Since Brainfuck is a rather difficult language to debug (citation needed),
an interactive debugger is included in the interpreter.  It is started
separately but runs on top of the same interpreter, and will output
commands as they're run and their effect on the tape.  It also supports 
instruction skipping (not sure why you'd want to do that?) and will be
extended in the future to do more debugging-related things.

### Translators

Right now, this program only supports generating a Brainfuck program that
prints a specified string.  It can, however, do so in a number of ways,
with varying degrees of optimization.  If I can ever find the code, there are
a handful of Brainfuck -> Python translators that can really speed up
execution (bad Python is better than good Brainfuck).
