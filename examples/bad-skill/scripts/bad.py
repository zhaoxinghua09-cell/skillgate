#!/usr/bin/env python3
"""A bad example script with lots of security issues."""
import os

# Hardcoded API key!
API_KEY = "sk-1234567890abcdefghijklmnop"

def dangerous_function(user_input):
    # Uses eval()!
    result = eval(user_input)
    return result

def run_command(cmd):
    # Uses os.system() with shell=True!
    os.system(cmd)

def main():
    user_input = input("Enter something: ")
    dangerous_function(user_input)

if __name__ == "__main__":
    main()
