#!/usr/bin/env python
"""
Common function libraries
"""

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
