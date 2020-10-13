#!/usr/bin/env python3

openFile = "examples/print8.ls8"
# openFile = "examples/call.ls8"
# openFile = "examples/interrupts.ls8"
# openFile = "examples/keyboard.ls8"
# openFile = "examples/mult.ls8"
# openFile = "examples/printstr.ls8"
# openFile = "examples/sctest.ls8"
# openFile = "examples/stack.ls8"
# openFile = "examples/stackoverflow.ls8"

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(openFile)
cpu.run()