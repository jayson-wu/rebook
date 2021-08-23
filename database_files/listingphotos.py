#!/usr/bin/env python
# https://www.postgresqltutorial.com/postgresql-python/

# -----------------------------------------------------------------------
# bookbag.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------
from sys import stderr

# takes database as input, creates a listingphotos table, returns True if
# executed properly, False if error occurred
def create(database):
    cursor = database._connection.cursor()
    commands = (
        'DROP TABLE IF EXISTS ListingPhotos',
        """
        CREATE TABLE ListingPhotos (
            public_id TEXT PRIMARY KEY,
            listing_id BIGINT NOT NULL,
            url TEXT NOT NULL
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

# inserts a row into the listingphotos table
def insert_row(database, info):
    command = 'INSERT INTO listingphotos (public_id, listing_id, url) ' + \
                'VALUES (%s, %s, %s)'
    return database._execute_command(command, info)

# updates a row in the listingphotos table
def update_row(database, info):
    command = 'UPDATE listingphotos ' + \
                'SET listing_id = %s, url = %s ' + \
                'WHERE public_id = %s'
    return database._execute_command(command, info)

# deletes a row from the listingphotos table
def delete_row(database, info):
    command = 'DELETE FROM listingphotos WHERE public_id = %s'
    return database._execute_command(command, info)