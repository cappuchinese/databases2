#!/usr/bin/python3

"""
Module DatabaseConnector:
    A class that connects the user to the database.
    Also contains methods to get the list of students and a list of results.
    Usage:
        python3 db_connector.py -h <host> -u <user> -d <database> -p
        If there are insufficient arguments given, the my.cnf file will be used by default.
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import sys
import mariadb
import argsparser


class DatabaseConnector:
    """
    This class makes a database connection.
    """
    def __init__(self):
        self.args = argsparser.dbcon_args()  # Execute the argsparser
        if len(sys.argv) < 9:  # Check if there are enough arguments
            print("Insufficient arguments to connect to database, "
                  "my.cnf file will be used for login instead")
            self.cnf_check = True

        self.conn, self.cur = self._connect()

    def _connect(self):
        """
        Connection method
        :return:
        """
        try:
            if self.cnf_check:  # If there are not enough arguments, use my.cnf file for connection
                connector = mariadb.connect(default_file="my.cnf")
            else:  # Connect with terminal commands
                connector = mariadb.connect(host=self.args.host, user=self.args.user,
                                            passwd=self.args.password, db=self.args.database)
            cursor = connector.cursor()

            print("Connected to database")
            return connector, cursor

        except mariadb.Error as err:
            print(f"Error with database:\n{err}")
            sys.exit(1)

    def call_genes(self):
        """
        Method to call the sp_get_genes procedure
        :return:
        """
        result = self.cur.callproc('sp_get_genes')
        return result

    def call_mtp(self):
        """
        Method to call the sp_get_tm_vs_probes procedure
        :return:
        """
        result = self.cur.callproc('sp_get_tm_vs_probes')
        return result

    def call_duplicates(self):
        """
        Method to call the sp_mark_duplicate_oligos procedure
        :return:
        """
        result = self.cur.callproc('sp_mark_duplicate_oligos')
        return result
