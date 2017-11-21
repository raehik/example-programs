#!/usr/bin/env python
#
# Short description of the program/script's operation/function.
#

import subprocess

def get_shell(cmd):
    """Run a shell command, blocking execution.

    Returns the exit code and stdout (respectively, as a tuple).
    """
    proc = subprocess.run(cmd, stdout=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode("utf-8").strip()

def run_shell(cmd):
    """Run a shell command without blocking execution (return
    immediately)."""
    subprocess.Popen(cmd)
    return True

def run_shell_interactive(cmd):
    """Run a shell command, blocking execution

    Doesn't touch stdout. Like dropping to shell during execution.

    Returns the exit code.
    """
    cmd = subprocess.run(cmd)
    return cmd.returncode

def yn_prompt(prompt):
    """Prompt the user with a yes/no question.

    @return 1 for "yes", 0 for "no", -1 for invalid input
    """
    ret_y = 1
    ret_n = 0
    ret_invalid = -1

    try:
        yn = input(prompt + " (y/n) ").lower()
    except KeyboardInterrupt:
        # new line so it looks better
        print()
        return ret_invalid
    except EOFError:
        return ret_invalid
    if yn == "y" or yn == "yes":
        return ret_y
    elif yn == "n" or yn == "no":
        return ret_n
    else:
        return ret_invalid

if __name__ == "__main__":
    print("This is a library, direct execution is disallowed.")
