#!/usr/bin/env python3
"""logging example module"""
import logging

# Levels
# 1. DEBUG: Detailed information, typically only of interest to a developer trying to diagnose a problem.
# 2. INFO: Confirmation that things are working as expected.
# 3. WARNING: An indication that something unexpected happened, or that a problem might occur in the near future
#       (e.g. ‘disk space low’). The software is still working as expected.
# 4. ERROR: Due to a more serious problem, the software has not been able to perform some function.
# 5. CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

logging.basicConfig(level=logging.DEBUG, filename="test.log", format="%(asctime)s: %(levelname)s: %(message)s")
print(logging.DEBUG)
def add(a, b):
    """add funtion"""
    return a + b

def sub(a, b):
    """div function"""
    return a - b

def mul(a, b):
    """mul function"""
    return a * b

def div(a, b):
    """div function"""
    return a / b

a = 10
b = 50

add_result = add(a, b)
sub_result = sub(a, b)
div_result = div(a, b)
mul_result = mul(a, b)

logging.debug(f"Add: {add_result}, sub: {sub_result}, div: {div_result}, mul: {mul_result}") 
