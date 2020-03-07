import collections
import os
import pathlib

import mysql.connector

from datetime import date, datetime, timedelta
from mysql.connector import errorcode

CONFIG = {
  'host': '127.0.0.1',
  'port': '3306',
  'user': 'root',
  'password': 'passwd',
  'raise_on_warnings': True
}

DB_NAME = 'employees'

TABLES = {}

TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

TABLES['departments'] = (
    "CREATE TABLE `departments` ("
    "  `dept_no` char(4) NOT NULL,"
    "  `dept_name` varchar(40) NOT NULL,"
    "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
    ") ENGINE=InnoDB")

TABLES['salaries'] = (
    "CREATE TABLE `salaries` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `salary` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['dept_emp'] = (
    "CREATE TABLE `dept_emp` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `dept_no` char(4) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['dept_manager'] = (
    "  CREATE TABLE `dept_manager` ("
    "  `dept_no` char(4) NOT NULL,"
    "  `emp_no` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`),"
    "  KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['titles'] = (
    "CREATE TABLE `titles` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `title` varchar(50) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date DEFAULT NULL,"
    "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

class MysqlModel(object):

    def __init__(self, cnx=None, cursor=None, g_employee=None, g_salary=None, tables={}):
        self.cnx = cnx
        self.cursor = cursor
        self.g_employee = g_employee
        self.g_salary = g_salary
        self.tables = tables

    def import_create_table_sqls(self, table_name='employees'):

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        SQL_DIR = 'app/sql'
        filename = 'create-' + table_name
        suffix = '.sql'
        file_path = pathlib.Path(base_dir, SQL_DIR, filename).with_suffix(suffix)

        with open(file_path, 'r') as sql_file:
            reader = sql_file.read()
        self.tables[table_name] = reader

    def connect_database(self, database='mysql'):
        try:
            self.cnx = mysql.connector.connect(**CONFIG)
            print("Connected to {}".format(database))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            # self.cnx.close()
            pass

    def check_database_existance(self):
        self.cursor = self.cnx.cursor()
        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                print("Database {} created successfully.".format(DB_NAME))
                self.cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

    def create_database(self):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
    
    def create_table(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
        # for table_name in self.tables:
        #     table_description = self.tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
    
    def get_data_employee(self):
        """
        first_name, last_name, hire_date, gender, birth_date
        """
        tomorrow = datetime.now().date() + timedelta(days=1)
        yield ('Harry', 'Potter', date(1999, 6, 22), 'M', date(2012, 3, 3))
        yield ('Harmaony', 'Granger', date(1999, 1, 2), 'M', date(1999, 12, 12))

    def get_data_salary(self):
        """
        emp_no, salary, from_date, to_date
        """
        tomorrow = datetime.now().date() + timedelta(days=1)
        yield ({'emp_no': 1,
                'salary': 65000,
                'from_date': date(1999, 4, 5),
                'to_date': date(2001, 12, 1),})
        yield ({'emp_no': 2,
                'salary': 40000,
                'from_date': date(1999, 2, 2),
                'to_date': date(2001, 1, 1),})

    def insert_data(self):
        # Define query for data insertion.
        add_employee = ("INSERT INTO employees "
                    "(first_name, last_name, hire_date, gender, birth_date) "
                    "VALUES (%s, %s, %s, %s, %s)")
        add_salary = ("INSERT INTO salaries "
                    "(emp_no, salary, from_date, to_date) "
                    "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

        # Get employee information
        if self.g_employee is None:
            self.g_employee = self.get_data_employee()
        data_employee = next(self.g_employee)

        # Insert new employee
        self.cursor.execute(add_employee, data_employee)
        emp_no = self.cursor.lastrowid

        # Get salary information
        if self.g_salary is None:
            self.g_salary = self.get_data_salary()
        data_salary = next(self.g_salary)

        """TODO Dynamically apply emp_no"""
        # if data_salary['emp_no'] is None:
        #     data_salary['emp_no'] = 4
        # print('emp_no', data_salary[emp_no], emp_no)
        # print('add_salary:', add_salary)
        # print('data_salary:', data_salary)

        # Insert salary information
        self.cursor.execute(add_salary, data_salary)
        self.cnx.commit()
        print('Inserting data: OK')

    def query_data(self):
        # SELECT first_name, last_name, hire_date FROM employees WHERE hire_date BETWEEN 1999-01-01 AND 1999-12-31
        query = ("SELECT first_name, last_name, hire_date FROM employees "
                "WHERE hire_date BETWEEN %s AND %s")

        hire_start = date(1999, 1, 1)
        hire_end = date(1999, 12, 31)

        self.cursor.execute(query, (hire_start, hire_end))

        for (first_name, last_name, hire_date) in self.cursor:
            print("{}, {} was hired on {:%d %b %Y}".format(
                last_name, first_name, hire_date))

    def drop_table(self, table_name):
        query = ("DROP TABLE IF EXISTS employees")
        query = ("DROP TABLE IF EXISTS %s")
        self.cursor.execute(query, table_name)
        # try:
        #     self.cursor.execute(query, table_name)
        # except:
        #     print("Table was not deleted")
        # else:
        #     print("Table {} has been deleted".format(talbe_name))

    def delete_database(self):
        query = ("DROP DATABASE %s")
        try:
            self.cursor.execute(query, (DB_NAME))
        except:
            print("Database was not deleted")
        else:
            print("Database {} has been deleted".format(DB_NAME))

    def close_database(self):
        try:
            self.cursor.close()
        except:
            print('Cursor already closed.')
        else:
            self.cnx.close()
            print('Connection closed.')

def main():
    mysqlmodel = MysqlModel()

    """Import create-database SQLs"""
    table_names = ['departments', 'dept_emp', 'dept_manager', 'employees', 'salaries', 'titles']
    for table_name in table_names:
        mysqlmodel.import_create_table_sqls(table_name)

    """Connect, Check"""
    mysqlmodel.connect_database()
    mysqlmodel.check_database_existance()

    """Create, Insert"""
    mysqlmodel.create_table()
    mysqlmodel.insert_data()
    mysqlmodel.insert_data()

    """Query"""
    mysqlmodel.query_data()

    """Drop Table"""
    # mysqlmodel.cursor.execute("DROP TABLE IF EXISTS employees")
    # for table in list(TABLES.keys()):
    #     print('table_name:', table)
    #     mysqlmodel.drop_table(table)

    """Delete Database"""
    # mysqlmodel.delete_database()

    """Conclude"""
    mysqlmodel.close_database()

if __name__ == "__main__":
    main()