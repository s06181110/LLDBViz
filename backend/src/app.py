#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Flask Test
"""

from flask import Flask, request, jsonify
from lldb_object import LLDBObject
import constants
app = Flask(__name__)

LLDB = LLDBObject()

@app.route('/')
def hello_world():
    """ hello world """
    return 'Hello, World!'

@app.route('/launch')
def launch_lldb():
    """ create lldb """
    LLDB.launch()
    static = LLDB.get_static_memory()
    memory = LLDB.get_stack_memory()
    register = LLDB.get_pointers()

    response = dict(
        memory = memory,
        static = static,
        register = register
    )
    return jsonify(response)

@app.route('/breakpoints', methods=['POST'])
def set_breakpoint():
    """ set a breakpoint """
    lines = request.json
    breakpoints = LLDB.set_breakpoint(lines)
    return breakpoints

@app.route('/process/<string:process>')
def debug_process(process):
    """ debugger process """
    LLDB.debug_process(process)
    if process == constants.STOP:
        return 'stop'

    static = LLDB.get_static_memory()
    memory = LLDB.get_stack_memory()
    register = LLDB.get_pointers()

    response = dict(
        memory = memory,
        static = static,
        register = register
    )
    return jsonify(response)

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
    from pprint import pprint
    LLDB.set_breakpoint([18])
    LLDB.launch()
    LLDB.debug_process('STEP_INTO')
    LLDB.get_stack_memory()

    # LLDB.debug_process('STEP_INTO')
    # LLDB.debug_process('STEP_INTO')
    # LLDB.get_address()
    # print(LLDB.get_variables())

if __name__ == "__main__":
    test()
