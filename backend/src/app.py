#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Flask Test
"""

from flask import Flask, request
from lldb_object import LLDBObject

app = Flask(__name__)

LLDB = LLDBObject()

@app.route('/')
def hello_world():
    """ hello world """
    return 'Hello, World!'

@app.route('/lldb')
def launch_lldb():
    """ create lldb """
    LLDB.launch()
    return "launch"

@app.route('/breakpoints', methods=['POST'])
def breakpoint():
    """ set a breakpoint """
    lines = request.json
    breakpoints = LLDB.set_breakpoint(lines)
    return breakpoints

@app.route('/memory')
def get_stack_memory():

    return LLDB.get_stack_memory()

@app.route('/process/<string:process>')
def debug_process(process):
    """ debugger process """
    LLDB.debug_process(process)
    return LLDB.get_stack_memory()

def test():
    """
    simple test
    this method called by main (is not related to serve)

    ex)
    set_breakpoint(11)
    launch_lldb()
    print(debug_process('STEP_INTO'))
    print(debug_process('STOP'))
    """
    

if __name__ == "__main__":
    test()
