#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Flask Test
"""

import os
# pylint: disable=E0401
import lldb  # export PYTHONPATH=`lldb -P`
from flask import Flask
from backend.lldb_object import LLDBObject

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

@app.route('/breakpoint/<int:line>')
def set_breakpoint(line):
    """ set a breakpoint """
    LLDB.set_breakpoint(line)
    return 'ok'

@app.route('/memory')
def get_stack_memory():
    " get current stack memory"
    return LLDB.get_stack_memory()
