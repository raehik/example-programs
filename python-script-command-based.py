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
        subparsers = self.parser.add_subparsers(title="commands", dest="command", metavar="[command]")
        subparsers.required = True

        subp_example = subparsers.add_parser("example-command",
                aliases=["example"],
                help="example command",
                description="Example command to show how to use subparsers.")
        subp_example.set_defaults(func=self.cmd_example_command)

        self.args = self.parser.parse_args()

        self.args.verbose += 1 # force some verbosity
        self._parse_verbosity()
    ## }}}

    def main(self):
        """Main entrypoint after program initialisation."""
        self.args.func()

    def cmd_example_command(self):
        return True

if __name__ == "__main__":
    program = Program()
    program.run()
