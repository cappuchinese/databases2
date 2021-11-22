#!/usr/bin/python3

"""
Module Tentamen:
    A class that takes a student and its results as arguments. This module can be initialized in
    both a script and as terminal command.
    Printing the class will return the given arguments in the console.
    Usage:
        As import: Tentamen(<student_name>, <course>, <date>, <grade>)
        In terminal: python3 Tentamen.py -s <student_name> -c <course> -d <date> -g <grade>
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import sys
import argsparser


class Tentamen:
    """
    This class contains information on a student's result of an exam.
    Class arguments:
        :param student: Name of the student
        :param vak: The name of the course
        :param datum: The date the exam was taken
        :param cijfer: The grade of the student
    """

    def __init__(self, student, vak, datum, cijfer):
        """
        Module to store the information on a student.
        See help(Tentamen) for more information
        """
        self.student = student
        self.vak = vak
        self.datum = datum
        self.cijfer = cijfer

    def __str__(self):
        """
        String representation returning the class instance
        :return:
        """
        return f"Student:\t{self.student}\nVak:\t{self.vak}\n" \
               f"Datum:\t{self.datum}\nCijfer:\t{self.cijfer}"


def main(args):
    exam = Tentamen(args.student_name, args.course, args.date, args.grade)
    print(exam)
    return 0


if __name__ == "__main__":
    exitcode = main(argsparser.tentamen_args())
    sys.exit(exitcode)
