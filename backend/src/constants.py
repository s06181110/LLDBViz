#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Constants file
"""

import os
# pylint: disable=E0401
import lldb

# assembler output
EXE = os.path.join(os.getcwd(), 'target', 'a.out')
ERROR = lldb.SBError()

# process
STEP_INTO = 'STEP_INTO'
STEP_OVER = 'STEP_OVER'
STEP_OUT  = 'STEP_OUT'
CONTINUE  = 'CONTINUE'
STOP      = 'STOP'
# LLDB symbols
TYPE_SYMBOLS = {
        lldb.eSymbolTypeAbsolute: 'Absolute',
        lldb.eSymbolTypeAdditional: 'Additional',
        lldb.eSymbolTypeBlock: 'Block',
        lldb.eSymbolTypeCode: 'Code',
        lldb.eSymbolTypeHeaderFile: 'Header File',
        lldb.eSymbolTypeCommonBlock: 'Common Block',
        lldb.eSymbolTypeCompiler: 'Compiler',
        lldb.eSymbolTypeException: 'Exception',
        lldb.eSymbolTypeData: 'Data',
        lldb.eSymbolTypeInstrumentation: 'Instrumentation',
        lldb.eSymbolTypeInvalid: 'Invalid',
        lldb.eSymbolTypeLineEntry: 'Line Entry',
        lldb.eSymbolTypeLineHeader: 'Line Header',
        lldb.eSymbolTypeLocal: 'Local',
        lldb.eSymbolTypeObjCClass: 'ObjC Class',
        lldb.eSymbolTypeObjCIVar: 'ObjC I Var',
        lldb.eSymbolTypeObjCMetaClass: 'ObjC Meta Class',
        lldb.eSymbolTypeObjectFile: 'Object File',
        lldb.eSymbolTypeParam: 'Param',
        lldb.eSymbolTypeReExported: 'Re Exported',
        lldb.eSymbolTypeResolver: 'Resolver',
        lldb.eSymbolTypeRuntime: 'Runtime',
        lldb.eSymbolTypeScopeBegin: 'Scope Begin',
        lldb.eSymbolTypeScopeEnd: 'Scope End',
        lldb.eSymbolTypeSourceFile: 'Source File',
        lldb.eSymbolTypeTrampoline: 'Trampoline',
        lldb.eSymbolTypeUndefined: 'Undefined',
        lldb.eSymbolTypeVariable: 'Variable',
        lldb.eSymbolTypeVariableType: 'VariableType',}
