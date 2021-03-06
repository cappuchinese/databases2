# Databases 2: Deelopdracht 01

Author: Lisa Hu<br>
Date: November 2021<br>
Version: 1.0

## Installation
To get this repository on your local server, use the following command:<br>
    `git clone https://github.com/cappuchinese/databases2.git`

To check if you got the latest version:<br>
    `git status`

To get the latest version:<br>
    `git pull`

Open the **my.cnf** file and modify the arrow brackets to personal login credentials.

From .zip:
1. Download the .zip
2. Unpack in target directory
3. Open the 'my.cnf' file and modify the arrow brackets to personal login credentials.
4. All setup, the code is runnable via command line.

This directory contains the following files:
* Tentamen.py
* db_connector.py
* my.cnf
* argsparser.py
* README.md
* README.txt

**Tentamen.py** defines a class "Tentamens" that stores information on a student's exam.<br>
**db_connector.py** defines a class "DatabaseConnector" that connects the user to a MariaDB database
using the **my.cnf** file. Besides connecting to the database, there are two more methods 
which can be called upon initializing the class.<br>
**argsparser.py** contains modules to parse the terminal commands for mentioned classes.

### Tentamen.py
A class that takes a student and its results as arguments. This module can be initialized in both 
a script and as terminal command.<br>Printing the class will return the given arguments in the console.
Usage:<br>
    As import: `Tentamen(<student_name>, <course>, <date>, <grade>)`<br>
    In terminal: `python3 Tentamen.py -s <student_name> -c <course> -d <date> -g <grade>`

### db_connector.py
A class that connects the user to the database. 
Also contains methods to get the list of students and a list of results.
Usage:
    `python3 db_connector.py -h <host> -u <user> -d <database> -p`
    If there are insufficient arguments given, the **my.cnf** file will be used by default.

### my.cnf
An option file. MariaDB can use this file as a login input to connect to the database.
To use this file, change everything between the arrow brackets (`<>`) to your personal login 
credentials respectively.