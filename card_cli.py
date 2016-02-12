#!/usr/bin/env python3
"""
An interactive shell interface to various functions
"""

import argparse
import inspect
import sys
import traceback
import types

################################################################################
# Create a parser for loading options on the interactive CLi
cli_parser = argparse.ArgumentParser()
cli_parser.add_argument('-s', action="store_true", dest="short",
        help="Shorten function names")
cli_args = cli_parser.parse_args()

################################################################################
# Create a custom ArgumentParser class for the interactive CLI

class ArgumentParser(argparse.ArgumentParser):
    """
    Local class to over-ride default ArgumentParser error function.
    """
    class Error(Exception):
        pass

    class TooFewArguments(Exception):
        pass

    def error(self, message):
        print("ERROR:", message)
        if "too few arguments" in message.lower():
            raise ArgumentParser.TooFewArguments(message)
        raise ArgumentParser.Error(message)

################################################################################
# Create argument parsers to hook into the various functions from the
# interactive shell

PARSERS = dict()

parser = ArgumentParser(prog='', add_help=False)
PARSERS['base'] = parser
subparsers = parser.add_subparsers(title='actions')

################################################################################

# Check the card_functions module for any interface functions that
# may be helpful for use in a CLI
import card_functions
CARD_FUNCTIONS = dict()
for thing in dir(card_functions):
    if thing.endswith("_card"):
        card_func = getattr(card_functions, thing)
        if type(card_func) == types.FunctionType:
            CARD_FUNCTIONS[thing] = {
                    "function": card_func,
                    "argspec": inspect.getargspec(card_func)
                    }

# Now check the card_set module for functions
import card_sets
SET_FUNCTIONS = dict()
for thing in dir(card_sets):
    set_func = getattr(card_sets, thing)
    if type(set_func) == types.FunctionType:
        SET_FUNCTIONS[thing] = {
                "function": set_func,
                "argspec": inspect.getargspec(set_func)
                }

################################################################################

def name_str(name):
    if cli_args.short:
        first, second = name.split('_', 1)
        if second == "card":
            return first[0:2]
        else:
            if '_' in second:
                second, third = second.split('_', 1)
                return "{}{}{}".format(first[0], second[0], third[0])
            else:
                return "{}{}".format(first[0], second[0])
    else:
        return name

def help_str(name, func):
    return "({0}) {1}".format(name, func.__doc__)

# Add a parser for each card function
for name, data in CARD_FUNCTIONS.items():
    sub_parser = subparsers.add_parser(name_str(name), add_help=False,
            help=help_str(name, data['function']))
    sub_parser.set_defaults(action=data['function'])
    for arg in data['argspec'].args:
        sub_parser.add_argument(arg)

    PARSERS[name] = sub_parser

# Add a parser for each card set function
for name, data in SET_FUNCTIONS.items():
    sub_parser = subparsers.add_parser(name_str(name), add_help=False,
            help=help_str(name, data['function']))
    sub_parser.set_defaults(action=data['function'])
    for arg in data['argspec'].args:
        sub_parser.add_argument(arg)

    PARSERS[name] = sub_parser

################################################################################

def execute(parsed_args):
    args_dict = vars(parsed_args)
    func = args_dict.pop('action')
    argstr = ','.join(map(
        lambda i: '='.join([i[0], str(i[1])]),
        args_dict.items()))

    try:
        ret = func(**args_dict)
        print("\n{0}({1}) returned: {2}".format(func.__name__, argstr, ret))
        return ret
    except Exception as e:
        print("\n{0}({1}) encountered an error: {2}\n".format(func.__name__, argstr, e))
        input("Press enter for traceback...")
        traceback.print_exc()
        print("")
        input("Press enter to continue...")

def get_help(action=None):
    try:
        parser = PARSERS[action]
    except KeyError:
        parser = PARSERS['base']
    return parser.format_help()

def quit(*args, **kwargs):
    print("Exiting...")
    exit(0)

# The quit option must be added after the quit function is defined
sub_parser = subparsers.add_parser('quit', add_help=False, help="Exit the interactive CLI")
sub_parser.set_defaults(action=quit)

################################################################################

# Primary loop
context = None
while True:

    prompt = "{line}{0}\n>>> ".format(get_help(context),
            line = "-"*80 + "\n"
            )

    user_input = input(prompt)
    context = None
    if len(user_input) == 0:
        continue

    try:
        args = parser.parse_args(user_input.split())

    # Don't quit on errors, just print a message and loop again
    except ArgumentParser.TooFewArguments as e:
        context = user_input.split()[0]
        continue
    except ArgumentParser.Error as e:
        continue

    execute(args)

