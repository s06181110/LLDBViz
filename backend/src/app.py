#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Flask Test
"""

from flask import Flask, request, jsonify
from lldb_object import LLDBObject
from memory_structure import MemoryStructure
from pprint import pprint
import constants
app = Flask(__name__)

LLDB = LLDBObject()
memory = MemoryStructure(LLDB)

@app.route('/')
def hello_world():
    """ hello world """
    return 'Hello, World!'

@app.route('/launch')
def launch_lldb():
    """ create lldb """
    memory.lldb = LLDB.launch()
    memory.update()
    return jsonify(memory.as_dict())

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
    if LLDB.is_active():
        memory.update()
    return jsonify(memory.as_dict())

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
    LLDB.set_breakpoint([27])
    launch_lldb()
    debug_process('STEP_INTO')

if __name__ == "__main__":
    test()
