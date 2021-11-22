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
from Tentamen import Tentamen


class DatabaseConnector:
    """
    This class makes a database connection.
    """

    def __init__(self):
        self.args, self.passwd = argsparser.dbcon_args()
        if len(self.args) < 4:
            print("Insufficient arguments to connect to database, "
                  "my.cnf file will be used for login instead")
            self.cnf_check = True

        self.conn, self.cur = self.connect()

    def connect(self):
        """
        Connection method
        :return:
        """
        try:
            if self.cnf_check:
                connector = mariadb.connect(default_file="my.cnf")
            else:
                connector = mariadb.connect(host=self.args.host, user=self.args.user,
                                            passwd=self.passwd, db=self.args.database)
            cursor = connector.cursor()

            return connector, cursor

        except mariadb.Error as err:
            print(f"Error with database:\n{err}")
            sys.exit(1)

    def get_student_list(self):
        """
        Method that returns a list of the students
        :return:
        """
        self.cur.execute("SELECT naam FROM studenten;")  # Execute the query
        records = self.cur.fetchall()  # Fetch the data
        student_list = [name for name in records]  # Put the data in a list

        return student_list

    def get_results_list(self):
        """
        Method to get the results of a student and stores it in Tentamen object
        :return:
        """
        query = "SELECT s.naam, c.naam, e.ex_datum, e.cijfer FROM examens e " \
                "JOIN studenten s ON s.stud_id = e.stud_id " \
                "JOIN cursussen c on e.cur_id = c.cur_id;"  # Set the query
        self.cur.execute(query)  # Execute the query
        records = self.cur.fetchall()  # Fetch the data
        objects = [Tentamen(*record) for record in records]  # Put records in a list
        return objects


if __name__ == "__main__":
    ing = DatabaseConnector()
