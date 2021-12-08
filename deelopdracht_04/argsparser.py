"""
Module to parse terminal commands
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import argparse
from getpass import getpass


def dbcon_args():
    """
    Parse terminal commands for DatabaseConnector module
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", metavar="", type=str, help="Host of database")
    parser.add_argument("-u", "--user", metavar="", type=str, help="Name of the user")
    parser.add_argument("-d", "--database", metavar="", type=str, help="Name of database")
    parser.add_argument("-p", "--password", action="store_true", dest="password",
                        help="Password of the user. OPTION ARGUMENT, NEW COMMAND PROMPT WILL OPEN.")
    args = parser.parse_args()

    # Hidden password
    if args.password:
        args.password = getpass("Enter password: ")

    # Return user given variables
    return args
