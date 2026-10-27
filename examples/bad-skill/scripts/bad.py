#!/usr/bin/env python3
"""A bad example script with lots of security issues.
   This is intentionally insecure for demonstration purposes only.
   DO NOT USE THIS CODE IN PRODUCTION.
"""
import os  # nosec B404

# Hardcoded API key!
API_KEY = "sk-1234567890abcdefghijklmnop"  # nosec B105

def dangerous_function(user_input):
    # Uses eval()!
    result = eval(user_input)  # nosec B307
    return result

def run_command(cmd):
    # Uses os.system() with shell=True!
    os.system(cmd)  # nosec B605

def main():
    user_input = input("Enter something:")
    dangerous_function(user_input)

if __name__ == "__main__":
    main()
