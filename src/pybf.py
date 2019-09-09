# -*- coding: utf-8 -*-
"""
PYBF - Python BrainFuck
A Brainfuck interpereter written in pure Python.

This interpereter has a few differences from classic Brainfuck:
 - the tape is infinite, both to the left and right (*see below)
 - it allows pause/resume and step-by-step debugging
 - it supports a 'console' similar to that of Python
 - it does not display program output until the program has terminated
   (subject to change in the future)

* When I say the tape is infinite, it is actually limited by the host OS's
  memory.  In a x32 system, I believe this is 2**31 cells total (which,
  although very large, is not infinite.)
"""

import io
import copy
import sys
import time

# use a dictionary as the 'array', because:
#  A. Python doesn't have a builtin array type (I know about the module!)
#  B. dictionary can be extended to have any number of values at will

__author__ = 'mishaturnbull'
__all__ = ["DEF_ARRAY", "DEF_VAL", "MAX_VAL", "ASCII", "R_ASCII", "CMDS",
           "bf_debugged", "clean_code", "buildbracemap",
           "println", "BF_Object", "execute", "step_debug", "start_console",
           "pointer", "watch", "EXAMPLES"]

DEF_ARRAY = {0: 0}
DEF_VAL = 0
MAX_VAL = 256
ASCII = dict(zip(range(MAX_VAL),
                 [chr(c) for c in range(MAX_VAL)]))
R_ASCII = dict(zip(ASCII.values(), ASCII.keys()))
CMDS = '+-.,><[]'

pointer = lambda n, s: s + '\n' + ' ' * ~-n + '^'


def bf_debugged(func):
    """Take a method of BF_Object and debug it."""

    def wrapped(cls):  # pylint: disable=C0111
        ret = func(cls)
        if cls.dbg:
            msg = cls.msgs[func.__name__]
            fmtd = msg.format(c=cls.cmdindex, pos=cls.pos, atpos=cls.a[cls.pos])
            print("PBF: {}".format(fmtd))
        return ret

    wrapped.__name__ = func.__name__
    wrapped.__doc__ = func.__doc__
    return wrapped


def clean_code(code):
    cleaned = ""
    for char in code:
        if char in CMDS:
            cleaned += char
    return cleaned


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[":
            temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap


def println(line):
    # Some platforms seem to have errors printing null character; use this
    # to not raise an error
    for char in line:
        if ord(char) == 0:
            print('.', end='')
        else:
            print(char, end='')
    print('')


class BF_Object(object):
    """The class where the magic happens.

    Takes input as Brainfuck code, optionally an input value, and
     optionally a boolean debug value.

    This class is where the Python code for the Brainfuck commands is;
     each command is of the form "cmd_{some 3 letter designator}"; the
     names can be accessed by `BF_Object.msgs.keys()`.

    On __init__, the code is cleaned and all variables are instantiated,
     a bracemap is built and a temporary stdout is created.

    On parse, the (cleaned) code is iterated through and the instruction
     characters are mapped to the BF_Object methods and added to a list called
     `BF_Object.instructions`.

    On execute, each instruction in `BF_Object.instructions` is executed.
    """

    msgs = {'cmd_INC': "{c:>3} |+| inc a[{pos}] = {atpos}",
            'cmd_DEC': "{c:>3} |-| dec a[{pos}] = {atpos}",
            'cmd_SHR': "{c:>3} |>| mov +1 to a[{pos}]",
            'cmd_SHL': "{c:>3} |<| mov -1 to a[{pos}]",
            'cmd_OUT': "{c:>3} |.| output {atpos}",
            'cmd_INP': "{c:>3} |,| input {atpos} -> a[{pos}]",
            'cmd_LBR': "{c:>3} |[| start loop at a[{pos}]",
            'cmd_RBR': "{c:>3} |]| end loop at a[{pos}]"}

    def __init__(self, code, input_val='', debug=False):
        """The base object of a Brainfuck program."""
        self.a = copy.deepcopy(DEF_ARRAY)
        self.pos = 0
        self.code = clean_code(code)
        self.instructions = []
        self.input_val = input_val
        self.cmdindex = 0
        self.bracemap = buildbracemap(self.code)
        self.dbg = debug
        self.stdout = io.StringIO("")

    def parse(self):
        """Parse a string into brainfuck instructions."""
        instructions_keys = {'+': self.cmd_INC,
                             '-': self.cmd_DEC,
                             '>': self.cmd_SHR,
                             '<': self.cmd_SHL,
                             '.': self.cmd_OUT,
                             ',': self.cmd_INP,
                             '[': self.cmd_LBR,
                             ']': self.cmd_RBR}
        for char in self.code:
            if char in instructions_keys:
                self.instructions.append(instructions_keys[char])

    def execute(self):
        """Execute the parsed instructions in brainfuck."""
        while self.cmdindex < len(self.instructions):
            self.execute_one()
            self.cmdindex += 1
        println(self.stdout.getvalue())

    def execute_one(self):
        """Execute one instruction."""
        self.instructions[self.cmdindex]()

    def onechr(self):
        while len(self.input_val) == 0:
            self.input_val = input('> ')
        parts = self.input_val[0], self.input_val[1:]
        self.input_val = parts[1]
        return parts[0]

    def printarray(self):
        a = list(self.a.values())
        # highlight the current cell
        a[self.pos] = '*{x}*'.format(x=self.a[self.pos])
        p = str(a)
        sys.stdout.write('\r{}'.format(p))
        sys.stdout.flush()

    @bf_debugged
    def cmd_INC(self):
        """+ instruction."""
        self.a[self.pos] = (self.a[self.pos] + 1) % MAX_VAL

    @bf_debugged
    def cmd_DEC(self):
        """- instruction."""
        prev = self.a[self.pos]
        if (prev - 1) < 0:
            new = MAX_VAL - 1
        else:
            new = prev - 1
        self.a[self.pos] = new

    @bf_debugged
    def cmd_SHR(self):
        """> instruction."""
        self.pos += 1
        if self.pos not in self.a:
            self.a.update({self.pos: DEF_VAL})

    @bf_debugged
    def cmd_SHL(self):
        """< instruction."""
        self.pos -= 1
        if self.pos not in self.a:
            self.a.update({self.pos: DEF_VAL})

    @bf_debugged
    def cmd_OUT(self):
        """. instruction."""
        self.stdout.write(ASCII[self.a[self.pos]])

    @bf_debugged
    def cmd_INP(self):
        """, instruction."""
        self.a[self.pos] = R_ASCII[self.onechr()]

    @bf_debugged
    def cmd_LBR(self):
        """[ instruction."""
        if self.a[self.pos] == 0:
            self.cmdindex = self.bracemap[self.cmdindex]
        else:
            pass

    @bf_debugged
    def cmd_RBR(self):
        """] instruction."""
        if self.a[self.pos] != 0:
            self.cmdindex = self.bracemap[self.cmdindex]
        else:
            pass


def execute(code, input_val='', debug=False):
    """Execute Brainfuck code, and return the tape when done."""
    bf = BF_Object(code, input_val=input_val, debug=debug)
    bf.parse()
    bf.execute()
    return bf.a


def execute_file(filename, input_val='', debug=False):
    with open(filename, "r") as f:
        bf = BF_Object(f.read(), input_val=input_val, debug=debug)
    bf.parse()
    bf.execute()
    return bf.a


def step_debug(code, input_val='', debug=True):
    """Execute Brainfuck code, printing the tape and index at each step.

    At each step, the user will be prompted for a command at the prompt "DBG> "
    They may enter:

        Command | Action
        --------+----------------------------------------------------------
        n       | Execute one instruction, move on to next
        q       | Terminate the program
        s       | Skip the instruction, move on to next
        e       | Execute the rest of the program with no more debugging
        w       | Execute the rest of the program at speed with debug info
        o       | Print the contents of the program's stdout file
    """

    bf = BF_Object(code, input_val=input_val, debug=debug)
    bf.parse()
    fmt = "PBF: {c:>3} | {a}[{i}]"
    fmts = lambda c, a, i: fmt.format(c=c, a=a, i=i)
    print(fmts('ini', bf.a, bf.pos))
    while bf.cmdindex < len(bf.instructions):
        print(pointer(bf.cmdindex, bf.code))
        cmd = input('DBG> ')[0]
        if cmd == "n":
            bf.execute_one()
            print(fmts(bf.cmdindex, bf.a, bf.pos))
            bf.cmdindex += 1
        elif cmd == "q":
            print("PBF: halted a={}".format(bf.a))
            break
        elif cmd == "s":
            bf.cmdindex += 1
        elif cmd == "e":
            while bf.cmdindex < len(bf.instructions):
                bf.execute_one()
                bf.cmdindex += 1
            break
        elif cmd == 'w':
            while bf.cmdindex < len(bf.instructions):
                bf.execute_one()
                print(fmts(bf.cmdindex, bf.a, bf.pos))
                bf.cmdindex += 1
                time.sleep(0.1)
        elif cmd == "o":
            println(bf.stdout.getvalue())
    println(bf.stdout.getvalue())


def watch(code, input_val='', delay=0.3):
    """Watch the tape being edited as Brainfuck code executes.  The currently
    selected cell is wrapped in `*`.

    Takes three arguments:
    str code:                  the Brainfuck code to be executed.
    optional str input_val:    an input value to be handed to code.
    optional float/int delay:  the delay in program step.
    """
    bf = BF_Object(code, input_val=input_val, debug=False)
    bf.parse()
    while bf.cmdindex < len(bf.instructions):
        bf.printarray()
        bf.execute_one()
        bf.cmdindex += 1
        time.sleep(delay)
    println(bf.stdout.getvalue())  # why doesnt this do anything?


def start_console():
    running = True
    while running:
        inp = input("PYBF> ")
        if inp.lower() in ['exit', 'quit', 'q']:
            print("Have a good day!")
            running = False
        else:
            execute(inp)

### Examples
#           (code, what it does)
EXAMPLES = [(',[>,]<[.<]', "Print the input, reversed."),
            (',[>+<-]', "Move data from a[0] to a[1]."),
            ('.+[.+]', "Print the ASCII character set.")]


if __name__ == '__main__':
    print("Doing stuff!")
    import sys
    print("Sys.argv: {}".format(sys.argv))
    try:
        codesnip = sys.argv[1:]
        codesnip = ''.join(codesnip)
    except IndexError:
        sys.exit(0)
    print("Code snippet: {}".format(codesnip))
    bfo = BF_Object(codesnip)
    bfo.parse()
    bfo.execute()
