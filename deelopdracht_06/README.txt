Author: Lisa Hu
Date: 28-02-22
Version: 1.0


NAME
Databases2 deelopdracht 06


DESCRIPTION
A short exercise for using stored procedures and bulk imports to a database and connecting it with a frontend


INSTALLATION
Make sure Python3.9 or newer is installed (https://www.python.org/downloads/) and the Python package "mariadb".
To install the package, execute the following command in the terminal:
	pip3 install mariadb
For executing the script, a connection with a database has to be made. Edit the my.cnf file to the correct login credentials.


FILES
main.py: A Python script that connects the database with the user. Using this script, the stored procedures in the database can be used. The stored procedures can be reached via terminal commands. To see the possible commands, use the following command:
	python3 main.py --help

deelopdracht06.sql: This SQL script contains all the tables, relations, imports and stored procedure.

my.cnf: Login credentials and host information for the database connection. Alter the chevrons to personal login credentials.

data (folder): A folder with dummy data for all the tables.


USAGE
First run the SQL script:
	mariadb deelopdracht06.sql

Call the Python script:
	python3 main.py <arguments>

The "--help" command shows all the possible arguments.


SUPPORT
May any problem occur, do not hesitate to contact me: l.j.b.hu@st.hanze.nl
