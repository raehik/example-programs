#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import sys, os, argparse, logging
import raehutils

class Program:
    def __init__(self):
        pass
    def __deinit(self):
        self.logger.debug("deinitialising...")

    ## CLI-related {{{
    def __init_logging(self):
        self.logger = logging.getLogger(os.path.basename(sys.argv[0]))
        lh = logging.StreamHandler()
        lh.setFormatter(logging.Formatter("%(name)s: %(levelname)s: %(message)s"))
        self.logger.addHandler(lh)

    def __parse_args(self):
        self.parser = argparse.ArgumentParser(description="Short description of the program/script's operation/function.")
        self.parser.add_argument("-v", "--verbose", help="be verbose", action="count", default=0)
        self.parser.add_argument("-q", "--quiet", help="be quiet (overrides -v)", action="count", default=0)
        self.parser.add_argument("posarg", help="positional argument")

        self.args = self.parser.parse_args()
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
        self.__init_logging()
        self.__parse_args()
        self.main()
        self.__deinit()
    ## }}}

    def fail(self, msg, ret):
        """Exit with a message and a return code.

        Should only be used for errors -- if you want to deinitialise and exit
        safely, simply return from main.
        """
        self.logger.error(msg)
        self.logger.debug("deinitialising...")
        self.__deinit()
        sys.exit(ret)

    def main(self):
        """Main entrypoint after program initialisation."""
        return True

if __name__ == "__main__":
    program = Program()
    program.run()
