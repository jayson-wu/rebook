#!/usr/bin/env python
# https://www.postgresqltutorial.com/postgresql-python/

# -----------------------------------------------------------------------
# booklistings.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------

from datetime import datetime
from database_files import bookbag
from sys import stderr

# takes database as input, creates a booklistings table, returns True if
# executed properly, False if error occurred
def create(database):
    cursor = database._connection.cursor()
    commands = (
        'DROP TABLE IF EXISTS BookListings',
        """
        CREATE TABLE BookListings (
            listing_id BIGSERIAL PRIMARY KEY,
            isbn BIGINT NOT NULL,
            seller TEXT NOT NULL,
            condition TEXT NOT NULL,
            price TEXT NOT NULL,
            seller_status TEXT NOT NULL,
            description TEXT,
            coursenum TEXT NOT NULL,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            time_created DOUBLE PRECISION NOT NULL
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

# inserts a row into the booklistings table
def insert_row(database, info):
    command = 'INSERT INTO booklistings (isbn, seller, condition, price, ' + \
                'seller_status, description, coursenum, title, authors, time_created) ' + \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING listing_id'
    return database._execute_command(command, info, return_id=True)

# updates a row in the booklistings table
def update_row(database, info):
    command = 'UPDATE booklistings ' + \
                'SET isbn = %s, seller = %s, condition = %s, price = %s, ' + \
                'seller_status = %s, description = %s, coursenum = %s, title = %s, ' + \
                'authors = %s, time_created = %s ' + \
                'WHERE listing_id = %s '
    return database._execute_command(command, info)

# deletes a row from the booklistings table
def delete_row(database, info):
    command = 'DELETE FROM booklistings WHERE listing_id = %s'
    return database._execute_command(command, info)

# helper method for getting listing ids
def _get_list(cursor):
    listings = []
    row = cursor.fetchone()
    while row:
        listings.append(row[0])
        row = cursor.fetchone()
    return listings

def get_active_listings(database, net_id):
    cursor = database._connection.cursor()
    QUERY = 'SELECT listing_id FROM booklistings ' + \
            'WHERE seller = %s AND seller_status = \'active\''
    cursor.execute(QUERY, (net_id,))
    listings = _get_list(cursor)
    cursor.close()
    return listings

def get_pending_listings(database, net_id):
    cursor = database._connection.cursor()
    QUERY = 'SELECT listing_id FROM booklistings ' + \
            'WHERE seller = %s AND seller_status = \'pending\''
    cursor.execute(QUERY, (net_id,))
    listings = _get_list(cursor)
    cursor.close()
    return listings

def get_completed_listings(database, net_id):
    cursor = database._connection.cursor()
    QUERY = 'SELECT listing_id FROM booklistings ' + \
            'WHERE seller = %s AND seller_status = \'completed\''
    cursor.execute(QUERY, (net_id,))
    listings = _get_list(cursor)
    cursor.close()
    return listings

# takes listing_id as input, returns dict of values (isbn, price, condition, title, authors, 
# coursenum, description, seller, seller_status, time_created, listing_id, formatted_time, in_bookbag)
def get(database, listing_id, user):
    cursor = database._connection.cursor()
    QUERY_STRING = 'SELECT isbn, price, condition, title, authors, coursenum, description, seller, seller_status, time_created ' + \
        'FROM "booklistings" ' + \
        'WHERE booklistings.listing_id = %s'
    cursor.execute(QUERY_STRING, [str(listing_id)])

    row = cursor.fetchone()
    cursor.close()

    cursor = database._connection.cursor()
    QUERY_STRING = 'SELECT public_id, url FROM "listingphotos" WHERE listingphotos.listing_id = %s'
    cursor.execute(QUERY_STRING, [str(listing_id)])
    photos = cursor.fetchall()
    cursor.close()

    if row is not None:
        rowdict = {'isbn': row[0], 'price': row[1], 'condition': row[2], 'title': row[3],
                    'authors': row[4], 'coursenum': row[5], 'description': row[6], 'seller': row[7], 
                    'seller_status': row[8], 'time_created': row[9],
                    'listing_id': listing_id, 'photos': photos}
        rowdict['formatted_time'] = datetime.fromtimestamp((int)(row[9]))
        rowdict['in_bookbag'] = bookbag.contains(database, user, listing_id)
        return rowdict
    else:
        return {}