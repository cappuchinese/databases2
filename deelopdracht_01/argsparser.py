"""
Module to parse terminal commands
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import argparse
from getpass import getpass


def tentamen_args():
    """
    Parse terminal commands for Tentamen module
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--student_name", type=str, metavar="S", required=True,
                        help="The name of the student")
    parser.add_argument("-c", "--course", type=str, metavar="C", required=True,
                        help="The name of the course")
    parser.add_argument("-d", "--date", type=str, metavar="D", required=True,
                        help="The date the exam was taken")
    parser.add_argument("-g", "--grade", type=float, metavar="G", required=True,
                        help="The grade the student was given")

    # Return user given variables
    return parser.parse_args()


def dbcon_args():
    """
    Parse terminal commands for DatabaseConnector
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", "--host", metavar="H", help="Host of database")
    parser.add_argument("-u", "--user", metavar="U", help="Name of the user")
    parser.add_argument("-d", "--database", metavar="D", help="Name of database")
    parser.add_argument("-p", "--password", action="store_true", dest="password",
                        help="Password of the user")
    args = parser.parse_args()

    if args.password:
        password = getpass("Enter password: ")

    return args, password
