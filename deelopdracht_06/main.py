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
        try:
            __conn = mariadb.connect(default_file="my.cnf")
            self.__cur = __conn.cursor()
            print("Connected to database")

        except mariadb.Error as err:
            sys.exit(err)

    def sp_get_genes(self):
        """
        Method to call the sp_get_genes procedure
        :return:
        """
        try:
            self.__cur.callproc('sp_get_genes')
            result = self.__cur.fetchall()
            return result
        except mariadb.Error as err:
            sys.exit(err)

    def sp_get_tm_vs_probes(self):
        """
        Method to call the sp_get_tm_vs_probes procedure
        :return:
        """
        try:
            self.__cur.callproc('sp_get_tm_vs_probes')
            result = self.__cur.fetchall()
            return result
        except mariadb.Error as err:
            sys.exit(err)

    def sp_mark_duplicate_oligos(self):
        """
        Method to call the sp_mark_duplicate_oligos procedure
        :return:
        """
        try:
            self.__cur.callproc('sp_mark_duplicate_oligos')
            print("Finished marking duplicates")
        except mariadb.Error as err:
            sys.exit(err)

    def sp_get_oligos_by_tm(self, min_tmp, max_tmp):
        """
        Method to call sp_get_oligos_by_tm procedure: Oligos between a min and max
        :param min_tmp: Minimum temperature of the oligos
        :param max_tmp: Maximum temperature of the oligos
        :return:
        """
        result_list = []
        try:
            self.__cur.callproc('sp_get_oligos_by_tm', (min_tmp, max_tmp))
            result = self.__cur.fetchall()
            for item in result:
                result_list.append(item)
            return result_list
        except mariadb.Error as err:
            sys.exit(err)

    def sp_get_matrices_by_quality(self):
        """
        Method to call sp_get_matrices_by_quality procedure: Show matrices by genes without probes
        :return:
        """
        result_list = []
        try:
            self.__cur.callproc('sp_get_matrices_by_quality')
            result = self.__cur.fetchall()
            for item in result:
                result_list.append(item)
            return result_list
        except mariadb.Error as err:
            sys.exit(err)

    def sp_create_probe(self, matrix_id, oligo_id):
        """
        Method to call sp_create_probe procedure: Create a new probe
        :param matrix_id: ID of the matrix
        :param oligo_id: ID of the oligo
        :return:
        """
        result_list = []
        try:
            self.__cur.callproc('sp_create_probe', (matrix_id, oligo_id))
            result = self.__cur.fetchall()
            for item in result:
                result_list.append(item)
        except mariadb.Error as err:
            sys.exit(err)

    def sp_create_matrix(self, melting_temp: int, difference: int):
        """
        Method to call sp_create_matrix procedure: Create matrix for probes between given temps
        :param melting_temp: Melting temperature
        :param difference: Marge of the temperature
        :return:
        """
        try:
            self.__cur.callproc('sp_create_matrix', (melting_temp, difference))
            min_tmp = melting_temp - difference
            max_tmp = melting_temp + difference
            print(f"Created a new matrix with probes between {min_tmp} and {max_tmp}")
        except mariadb.Error as err:
            sys.exit(err)
