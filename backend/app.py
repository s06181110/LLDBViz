#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Flask Test
"""

import os
# pylint: disable=E0401
import lldb  # export PYTHONPATH=`lldb -P`
from flask import Flask

app = Flask(__name__)

EXE = os.path.join(os.getcwd(), 'target', 'a.out')

# Create a new debugger instance
debugger = lldb.SBDebugger.Create()
debugger.SetAsync (False)

target = debugger.CreateTarget(EXE)
error_ref = lldb.SBError()
process = None

@app.route('/')
def hello_world():
    """ hello world """
    return 'Hello, World!'

@app.route('/lldb')
def launch_lldb():
    """ create lldb """
    print(os.getcwd())
    global process
    process = target.LaunchSimple (None, None, os.getcwd())
    return "launch"

@app.route('/breakpoint/<int:line>')
def set_breakpoint(line):
    """ set a breakpoint """
    target.BreakpointCreateByLocation("main.c", line)
    return 'ok'

@app.route('/memory')
def get_stack_memory():
    " get current stack memory"
    global process
    thread = process.GetThreadAtIndex(0)
    frame = thread.GetFrameAtIndex(0)
    init_addr = frame.GetSP()
    stack_memory = process.ReadMemory(init_addr, 0x20, error_ref)
    print(stack_memory)
    memory_int = stack_memory.hex()
    top  = 0
    for byte in range(8, len(memory_int) + 1, 8):
        print("{}: {}".format(hex(init_addr+int(byte/2)), memory_int[top:byte]))
        top = byte
    return "memory:\n {}".format(stack_memory.hex())
