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
import argparse
import mariadb


class DatabaseConnector:
    """
    This class makes a database connection.
    """
    def __init__(self):
        """
        Initializing the database connection
        """
        self.__conn, self.__cur = self.__connect()

    @staticmethod
    def __connect():
        """
        Connection method
        :return: Database connector and cursor
        """
        try:
            connector = mariadb.connect(default_file="my.cnf")
            cursor = connector.cursor()
            print("Connected to database")
            return connector, cursor

        except mariadb.Error as err:
            print(f"Error with database:\n{err}")
            sys.exit(1)

    def sp_get_genes(self):
        """
        Method to call the sp_get_genes procedure
        :return:
        """
        result = self.__cur.callproc('sp_get_genes')
        return result

    def sp_get_tm_vs_probes(self):
        """
        Method to call the sp_get_tm_vs_probes procedure
        :return:
        """
        result = self.__cur.callproc('sp_get_tm_vs_probes')
        return result

    def sp_mark_duplicate_oligos(self):
        """
        Method to call the sp_mark_duplicate_oligos procedure
        :return:
        """
        result = self.__cur.callproc('sp_mark_duplicate_oligos')
        return result

    def sp_get_oligos_by_tm(self, min_tmp, max_tmp):
        """
        Method to call sp_get_oligos_by_tm procedure: Oligos between a min and max
        :param min_tmp: Minimum temperature of the oligos
        :param max_tmp: Maximum temperature of the oligos
        :return:
        """
        result = self.__cur.callproc('sp_get_oligos_by_tm', (min_tmp, max_tmp))
        return result

    def sp_get_matrices_by_quality(self):
        """
        Method to call sp_get_matrices_by_quality procedure: Show matrices by genes without probes
        :return:
        """
        result = self.__cur.callproc('sp_get_matrices_by_quality')
        return result

    def sp_create_probe(self, matrix_id, oligo_id):
        """
        Method to call sp_create_probe procedure: Create a new probe
        :param matrix_id: ID of the matrix
        :param oligo_id: ID of the oligo
        :return:
        """
        result = self.__cur.callproc('sp_create_probe', (matrix_id, oligo_id))
        return result
