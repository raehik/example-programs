#!/usr/bin/env python
#
# Short description of the program/script's operation/function.
#

import subprocess
import time

def get_shell(cmd):
    """Run a shell command, blocking execution, detaching stdin, stdout and
    stderr.

    Useful for grabbing shell command outputs, or if you want to run something
    silently and wait for it to finish.

    @return the command's return code, stdout and stderr (respectively, as a
            tuple).
    """
    proc = subprocess.run(cmd, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return proc.returncode, \
           proc.stdout.decode("utf-8").strip(), \
           proc.stderr.decode("utf-8").strip()

def get_shell_with_input(cmd, s):
    """Run a shell command, blocking execution, detaching stdin, stdout and
    stderr.

    Takes an argument to use as the string to pass to stdin. Puts a newline on
    the end, because that appears to be important for some/many programs (bc at
    least). TODO.

    @return the command's return code, stdout and stderr (respectively, as a
            tuple).
    """
    proc = subprocess.run(cmd, input=bytes("{}\n".format(s), "utf-8"),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return proc.returncode, \
           proc.stdout.decode("utf-8").strip(), \
           proc.stderr.decode("utf-8").strip()

def drop_to_shell(cmd):
    """Run a shell command, blocking execution.

    Doesn't touch any pipes. Like dropping to shell during execution.

    @return the command's exit code
    """
    proc = subprocess.run(cmd)
    return proc.returncode

def run_shell_detached(cmd):
    """Run a shell command, not blocking execution (returns immediately),
    detaching stdin, stdout and stderr.

    Not ideal: only seems to properly detach after script exits (otherwise, a
    Ctrl-C can interrupt it). See this SE question (tl;dr deal with signals, or
    daemonise): https://stackoverflow.com/questions/37058013

    Will generally be fine in cases when the script ends very soon after this
    function is called.
    """
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)

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
