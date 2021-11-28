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

    def get_student_list(self):
        """
        Method that returns a list of the students
        :return:
        """
        self.cur.execute("SELECT naam FROM studenten;")  # Execute the query
        records = self.cur.fetchall()  # Fetch the data
        student_list = [name[1] for name in records]  # Put the data in a list

        return student_list

    def get_results_list(self, student):
        """
        Method to get the results of a student and stores it in Tentamen object
        :param student: name of the student in the table
        :return:
        """
        try:
            query = "SELECT s.naam, c.naam, e.ex_datum, e.cijfer FROM examens e " \
                    "JOIN studenten s ON s.stud_id = e.stud_id " \
                    "JOIN cursussen c ON e.cur_id = c.cur_id " \
                    "WHERE s.naam = %s;"  # Set the query
            self.cur.execute(query, (student,))  # Execute the query
            records = self.cur.fetchall()  # Fetch the data
            objects = [Tentamen(*record) for record in records]  # Put records in a list
        except mariadb.OperationalError:
            print("Operational Error, could not get records on exams.")
            sys.exit(1)

        return objects


def main():
    """
    Main function of the script
    :return 0: exit code
    """
    connector = DatabaseConnector()  # Initialize class -> connect to database
    print(connector.get_student_list())  # Print the list of students

    # Ask to get exams from which student
    student_name = input("Which student do you want to return its results?\n>")
    exams = connector.get_results_list(student_name)  # Get the exams
    for exam in exams:
        print(exam)  # Print the results of each exam

    return 0


if __name__ == "__main__":
    sys.exit(main())
