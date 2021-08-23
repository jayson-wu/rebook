#!/usr/bin/env python
# https://www.postgresqltutorial.com/postgresql-python/

# -----------------------------------------------------------------------
# purchases.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------

# takes database as input, creates a purchases table, returns True if
# executed properly, False if error occurred
def create(database):
    cursor = database._connection.cursor()
    commands = (
        'DROP TABLE IF EXISTS Purchases',
        """
        CREATE TABLE Purchases (
            listing_id BIGINT PRIMARY KEY,
            buyer TEXT NOT NULL,
            buyer_status TEXT NOT NULL
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

# inserts a row into the purchases table


def insert_row(database, info):
    command = 'INSERT INTO purchases (listing_id, buyer, buyer_status) ' + \
        'VALUES (%s, %s, %s)'
    return database._execute_command(command, info)

# updates a row in the purchases table


def update_row(database, info):
    command = 'UPDATE purchases ' + \
        'SET buyer_status = %s ' + \
        'WHERE listing_id = %s '
    return database._execute_command(command, info)

# deletes a row from the purchases table


def delete_row(database, info):
    command = 'DELETE FROM purchases WHERE listing_id = %s'
    return database._execute_command(command, info)

# get the buyer of the book


def get_buyer(database, listing_id):
    cursor = database._connection.cursor()
    QUERY_STRING = 'SELECT buyer FROM purchases WHERE listing_id = %s'
    cursor.execute(QUERY_STRING, (listing_id,))
    row = cursor.fetchone()
    if row:
        buyer_id = row[0]
    else:
        buyer_id = None

    cursor.close()

    return buyer_id