Databases 2: Deelopdracht 01

Author: Lisa Hu
Date: November 2021
Version: 1.0

This directory contains the following files:
* Tentamen.py
* db_connector.py
* my.cnf
* argsparser.py
* README.md
* README.txt

Tentamen.py defines a class "Tentamens" that stores information on a student's exam.
db_connector.py defines a class "DatabaseConnector" that connects the user to a MariaDB databaseusing the my.cnf file. Besides connecting to the database, there are two more methods which can be called upon initializing the class.
argsparser.py contains modules to parse the terminal commands for mentioned classes.

Tentamen.py
A class that takes a student and its results as arguments. This module can be initialized in both a script and as terminal command.
Printing the class will return the given arguments in the console.
Usage:<br>
    As import: Tentamen(<student_name>, <course>, <date>, <grade>)
    In terminal: python3 Tentamen.py -s <student_name> -c <course> -d <date> -g <grade>

db_connector.py
A class that connects the user to the database. 
Also contains methods to get the list of students and a list of results.
Usage:
    python3 db_connector.py -h <host> -u <user> -d <database> -p
    If there are insufficient arguments given, the my.cnf file will be used by default.

my.cnf
An option file. MariaDB can use this file as a login input to connect to the database.
To use this file, change everything between the arrow brackets ('<>') to your personal login credentials respectively.