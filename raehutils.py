#!/usr/bin/env python
#
# Common functions and behaviour that raehik uses, cleaned up and placed in a
# standalone module.
#

import sys, os, logging, subprocess

class RaehBaseClass:
    def _deinit(self):
        self.logger.debug("deinitialising...")

    ## CLI-related {{{
    def _init_logging(self):
        self.logger = logging.getLogger(os.path.basename(sys.argv[0]))
        lh = logging.StreamHandler()
        lh.setFormatter(logging.Formatter("%(name)s: %(levelname)s: %(message)s"))
        self.logger.addHandler(lh)

    def _parse_verbosity(self):
        if self.args.verbose == 1:
            self.logger.setLevel(logging.INFO)
        elif self.args.verbose >= 2:
            self.logger.setLevel(logging.DEBUG)
        if self.args.quiet >= 1:
            # reset verbosity (to make verbose/quiet checks easier)
            self.args.verbose = 0
            self.logger.setLevel(logging.NOTSET)

    def run(self):
        """Run from CLI: parse arguments, run main, deinitialise."""
        self._init_logging()
        self._parse_args()
        self.main()
        self._deinit()
    ## }}}

    def fail(self, msg, ret):
        """Exit with a message and a return code.

        Should only be used for errors -- if you want to deinitialise and exit
        safely, simply return from main.
        """
        self.logger.error(msg)
        self._deinit()
        sys.exit(ret)

    def fail(self):
        """Exit with a generic message and return code.

        Should be used for internal functions that the user doesn't need to know
        about. Generally indicates a logic error, rather than an input one.
        """
        self.fail("internal error", 1)

# ------------

def get_shell(cmd, cwd=None):
    """Run a shell command, blocking execution, detaching stdin, stdout and
    stderr.

    Useful for grabbing shell command outputs, or if you want to run something
    silently and wait for it to finish.

    @param cmd command to run as an array, where each element is an argument
    @param cwd if present, directory to use as CWD
    @return the command's return code, stdout and stderr (respectively, as a
            tuple)
    """
    proc = subprocess.run(cmd, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=cwd)
    return proc.returncode, \
           proc.stdout.decode("utf-8").strip(), \
           proc.stderr.decode("utf-8").strip()

def get_shell_with_input(cmd, stdin_in, cwd=None):
    """Run a shell command with a given string passed to stdin, blocking
    execution and detaching stdout and stderr.

    We put a newline on the end of stdin_in, because that appears to be important for
    some programs (e.g. bc). TODO though, unsure. Maybe should be an option.

    @param cmd    command to run as an array, where each element is an argument
    @param std_in string to pass to stdin
    @param cwd    if present, directory to use as CWD
    @return the command's return code, stdout and stderr (respectively, as a
            tuple)
    """
    proc = subprocess.run(cmd, input=bytes("{}\n".format(stdin_in), "utf-8"),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=cwd)
    return proc.returncode, \
           proc.stdout.decode("utf-8").strip(), \
           proc.stderr.decode("utf-8").strip()

def drop_to_shell(cmd, cwd=None):
    """Run a shell command, blocking execution.

    Doesn't touch any pipes. Like dropping to shell during execution.

    @param cmd command to run as an array, where each element is an argument
    @param cwd if present, directory to use as CWD
    @return the command's exit code
    """
    return subprocess.run(cmd, cwd=cwd).returncode

def run_shell_detached(cmd, cwd=None):
    """Run a shell command, not blocking execution (returns immediately),
    detaching stdin, stdout and stderr.

    Not ideal: only seems to properly detach after script exits (otherwise, a
    Ctrl-C can interrupt it). See this SE question (tl;dr deal with signals, or
    daemonise): https://stackoverflow.com/questions/37058013

    Will generally be fine in cases when the script ends very soon after this
    function is called.

    @param cmd command to run as an array, where each element is an argument
    @param cwd if present, directory to use as CWD
    """
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL,
                          cwd=cwd)

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
