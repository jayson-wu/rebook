#!/usr/bin/env python
# https://www.postgresqltutorial.com/postgresql-python/

# -----------------------------------------------------------------------
# bookbag.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------
from sys import stderr

# takes database as input, creates a bookbag table, returns True if
# executed properly, False if error occurred
def create(database):
    cursor = database._connection.cursor()
    commands = (
        'DROP TABLE IF EXISTS Bookbag',
        """
        CREATE TABLE Bookbag (
            buyer TEXT NOT NULL,
            listing_id BIGINT NOT NULL,
            listing_status TEXT NOT NULL,
            PRIMARY KEY (buyer , listing_id)
        )
        """
    )

    for command in commands:
        try:
            cursor.execute(command)
            print("EXECUTED: " + str(command))
        except Exception as e:
            print(str(e), file=stderr)
            return False

    cursor.close()
    database._connection.commit()
    return True

# inserts a row into the bookbag table
def insert_row(database, info):
    command = 'INSERT INTO bookbag (buyer, listing_id, listing_status) ' + \
                'VALUES (%s, %s, %s)'
    return database._execute_command(command, info)

# updates a row in the bookbag table
def update_row(database, info):
    command = 'UPDATE bookbag ' + \
                'SET listing_status = %s ' + \
                'WHERE buyer = %s, listing_id = %s'
    return database._execute_command(command, info)

# deletes a row from the bookbag table
def delete_row(database, info):
    command = 'DELETE FROM bookbag WHERE buyer = %s AND listing_id = %s'
    return database._execute_command(command, info)

# Checks whether listing with listing_id is in the bookbag of buyer
def contains(database, buyer, listing_id):
    cursor = database._connection.cursor()
    QUERY_STRING = 'SELECT * FROM bookbag WHERE buyer = %s AND listing_id = %s'
    cursor.execute(QUERY_STRING, (buyer, listing_id))
    row = cursor.fetchone()
    cursor.close()
    if row is not None:
        return True
    return False

# change the listing_status of all books in the bookbag with listing_id to status
def change_status(database, listing_id, status):
    QUERY_STRING = 'UPDATE bookbag SET listing_status = %s WHERE listing_id = %s'
    return database._execute_command(QUERY_STRING, [status, listing_id])