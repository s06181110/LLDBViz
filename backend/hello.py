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

EXE = "./target/a.out"

# Create a new debugger instance
debugger = lldb.SBDebugger.Create()
debugger.SetAsync (False)

target = debugger.CreateTarget(EXE)
error_ref = lldb.SBError()

@app.route('/')
def hello_world():
    """ hello world """
    return 'Hello, World!'

@app.route('/lldb')
def launch_lldb():
    """ create lldb """
    print(os.getcwd())
    process = target.LaunchSimple (None, None, os.getcwd())
    print(process.GetState())
    return "launch"

@app.route('/breakpoint/<int:line>')
def set_breakpoint(line):
    """ set a breakpoint """
    target.BreakpointCreateByLocation("main.c", line)
    return 'ok'
