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


def main():
    """
    Main run
    :return:
    """
    # Arguemnts
    parser = argparse.ArgumentParser(description="Connect to database to control the procedures")
    parser.add_argument("-g", "--sp_get_genes", action="store_true", dest="get_genes",
                        help="Get a list of all the genes")
    parser.add_argument("-to", "--sp_get_tm_vs_oligos", action="store_true", dest="tm_oligo",
                        help="The different melting temps divided by oligonucleotides")
    parser.add_argument("-d", "--sp_mark_duplicate_oligos", action="store_true", dest="duplicates",
                        help="Mark all the duplicate oligos")
    parser.add_argument("-ot", "--sp_get_oligos_by_tm", dest="oligos_by_tmp", nargs=2,
                        help="Get the oligonucleotides within the given temperatures")
    parser.add_argument("-mq", "--sp_get_matrices_by_quality", action="store_true", dest="mat_qual",
                        help="Show matrices ordered by genes without probes")
    parser.add_argument("-cp", "--sp_create_probe", nargs=2, dest="probe",
                        help="Create a new probe")
    parser.add_argument("-cm", "--sp_create_matrix", nargs=2, dest="matrix",
                        help="Create matrix for probes between given temperatures")

    # Parse arguments
    args = parser.parse_args()
    # Initialize connection
    db_mod = DatabaseConnector()

    # Return wanted results
    if args.get_genes:
        genes = db_mod.sp_get_genes()
        # Output formatting
        for row in genes:
            print(f"Gene: {row[0]}, identifier: {row[1]}, seq: {row[2]}")
    elif args.tm_oligo:
        temps = db_mod.sp_get_tm_vs_probes()
        print(f"Amount of unique melting point per oligo: {temps}")
    elif args.duplicates:
        db_mod.sp_mark_duplicate_oligos()
    elif args.oligos_by_tmp:
        print(db_mod.sp_get_oligos_by_tm(args.oligos_by_tmp[0], args.oligos_by_tmp[1]))
    elif args.mat_qual:
        print(db_mod.sp_get_matrices_by_quality())
    elif args.probe:
        print(db_mod.sp_create_probe(args.probe[0], args.probe[1]))
    elif args.matrix:
        db_mod.sp_create_matrix(args.matrix[0], args.matrix[1])
    else:
        sys.exit("Choose a procesure to execute. Exiting program...")

    return 0


if __name__ == '__main__':
    EXITCODE = main()
    sys.exit(EXITCODE)
