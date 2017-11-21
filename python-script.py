#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import sys, os, argparse, logging
from raehutils import *

class Program:
    ## __init_logging, run, exit {{{
    def __init_logging(self):
        self.logger = logging.getLogger(os.path.basename(sys.argv[0]))
        lh = logging.StreamHandler()
        lh.setFormatter(logging.Formatter("%(name)s: %(levelname)s: %(message)s"))
        self.logger.addHandler(lh)

    def run(self):
        """Run from CLI: parse arguments, run main."""
        self.__init_logging()
        self.__parse_args()
        self.main()

    def exit(self, msg, ret):
        """Exit with explanation."""
        self.logger.error(msg)
        sys.exit(ret)
    ## }}}

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
            self.logger.setLevel(logging.NOTSET)

    def main(self):
        """Main entrypoint after program setup."""
        return True

if __name__ == "__main__":
    program = Program()
    program.run()
