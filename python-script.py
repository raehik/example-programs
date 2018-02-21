#!/usr/bin/env python3
#
# Short description of the program/script's operation/function.
#

import raehutils
import sys, os, argparse, logging

class Program(raehutils.RaehBaseClass):
    def __init__(self):
        pass

    def _deinit(self):
        self.logger.debug("deinitialising...")

    ## CLI-related {{{
    def _parse_args(self):
        self.parser = argparse.ArgumentParser(description="Short description of the program/script's operation/function.")
        self.parser.add_argument("-v", "--verbose", help="be verbose", action="count", default=0)
        self.parser.add_argument("-q", "--quiet", help="be quiet (overrides -v)", action="count", default=0)
        self.parser.add_argument("posarg", help="positional argument")

        self.args = self.parser.parse_args()

        #self.args.verbose += 1 # force some verbosity
        self._parse_verbosity()
    ## }}}

    def main(self):
        """Main entrypoint after program initialisation."""
        return True

if __name__ == "__main__":
    program = Program()
    program.run()
