#!/usr/bin/env python3
"""
An interactive shell interface to various functions
"""

import argparse
import inspect
import traceback
import types

import card_functions
import card_sets

################################################################################
# Create a parser for loading options on the interactive CLi
CLI_PARSER = argparse.ArgumentParser()
CLI_PARSER.add_argument('-s', action="store_true", dest="short",
                        help="Shorten function names")
CLI_ARGS = CLI_PARSER.parse_args()

################################################################################
# Create a custom ArgumentParser class for the interactive CLI

class ArgumentParser(argparse.ArgumentParser):
    """
    Local class to over-ride default ArgumentParser error function.
    """
    class Error(Exception):
        """
        A custom error class for catching only the exceptions we can handle.
        """
        pass

    class TooFewArguments(Exception):
        """
        A custom error class for indicating some help docs are needed.
        """
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

PARSER = ArgumentParser(prog='', add_help=False)
PARSERS['base'] = PARSER
SUBPARSERS = PARSER.add_subparsers(title='actions')

################################################################################

# Check the card_functions module for any interface functions that
# may be helpful for use in a CLI
CARD_FUNCTIONS = dict()
for thing in dir(card_functions):
    if thing.endswith("_card"):
        card_func = getattr(card_functions, thing)
        if isinstance(card_func, types.FunctionType):
            # pylint: disable=deprecated-method
            # Complaining about getargspec being deprecated
            CARD_FUNCTIONS[thing] = {
                "function": card_func,
                "argspec": inspect.getargspec(card_func)
                }

# Now check the card_set module for functions
SET_FUNCTIONS = dict()
for thing in dir(card_sets):
    set_func = getattr(card_sets, thing)
    if isinstance(set_func, types.FunctionType):
        # pylint: disable=deprecated-method
        # Complaining about getargspec being deprecated
        SET_FUNCTIONS[thing] = {
            "function": set_func,
            "argspec": inspect.getargspec(set_func)
            }

################################################################################

def name_str(func_name):
    """
    Return an action name for the function. By default this is just the function
    name unless the interactive CLI script gets the '-s' option.
    """
    if CLI_ARGS.short:
        first, second = func_name.split('_', 1)
        if second == "card":
            return first[0:2]
        else:
            if '_' in second:
                second, third = second.split('_', 1)
                return "{}{}{}".format(first[0], second[0], third[0])
            else:
                return "{}{}".format(first[0], second[0])
    else:
        return func_name

def help_str(func):
    """
    Create a help string for an action from the corresponding functions name and
    doc string.
    """
    return "({0}) {1}".format(func.__name__, func.__doc__)

# Add a parser for each card function
for name, data in CARD_FUNCTIONS.items():
    sub_parser = SUBPARSERS.add_parser(name_str(name), add_help=False,
                                       help=help_str(data['function']))
    sub_parser.set_defaults(action=data['function'])
    for arg in data['argspec'].args:
        sub_parser.add_argument(arg)

    PARSERS[name] = sub_parser

# Add a parser for each card set function
for name, data in SET_FUNCTIONS.items():
    sub_parser = SUBPARSERS.add_parser(name_str(name), add_help=False,
                                       help=help_str(data['function']))
    sub_parser.set_defaults(action=data['function'])
    for arg in data['argspec'].args:
        sub_parser.add_argument(arg)

    PARSERS[name] = sub_parser

################################################################################

def execute(parsed_args):
    """
    Use the interactive CLI arguments to execute the corresponding function
    """
    args_dict = vars(parsed_args)
    func = args_dict.pop('action')
    # pylint: disable=bad-builtin
    # Complaining about using map
    argstr = ','.join(map(
        lambda i: '='.join([i[0], str(i[1])]),
        args_dict.items()))

    try:
        ret = func(**args_dict)
        print("\n{0}({1}) returned: {2}".format(func.__name__, argstr, ret))
        return ret

    # pylint: disable=broad-except
    # Intentionally catching all exceptions to prevent interactive CLI from
    # exiting
    except Exception as error:
        print("\n{0}({1}) encountered an error: {2}\n".format(
            func.__name__, argstr, error))
        input("Press enter for traceback...")
        traceback.print_exc()
        print("")
        input("Press enter to continue...")

def get_help(action=None):
    """
    Depending on the action specified, get the help output from the
    corresponding action parser.
    """
    try:
        parser = PARSERS[action]
    except KeyError:
        parser = PARSERS['base']
    return parser.format_help()

# pylint: disable=redefined-outer-name, unused-argument
# The *args, **kwargs format is necessary due to how ArgumentParser objects
# call action functions, but are not necessary for exiting.
def exit_shell(*args, **kwargs):
    """
    Exit the interactive CLI
    """
    print("Exiting...")
    exit(0)

# The quit option must be added after the quit function is defined
SUB_PARSER = SUBPARSERS.add_parser('quit', add_help=False, help="Exit the interactive CLI")
SUB_PARSER.set_defaults(action=exit_shell)

################################################################################

# Primary loop
CONTEXT = None
while True:

    PROMPT = "{line}{0}\n>>> ".format(get_help(CONTEXT),
                                      line="-"*80 + "\n")

    USER_INPUT = input(PROMPT)
    CONTEXT = None
    if len(USER_INPUT) == 0:
        continue

    try:
        ARGS = PARSER.parse_args(USER_INPUT.split())

    # Don't quit on errors, just print a message and loop again
    except ArgumentParser.TooFewArguments:
        CONTEXT = USER_INPUT.split()[0]
        continue
    except ArgumentParser.Error:
        continue

    execute(ARGS)

