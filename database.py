#!/usr/bin/env python
# https://www.postgresqltutorial.com/postgresql-python/

# -----------------------------------------------------------------------
# database.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------

import os
import psycopg2
from sys import stderr
import time
from datetime import datetime
from database_files import booklistings, bookbag, purchases, listingphotos

# -----------------------------------------------------------------------


class Database:

    def __init__(self):
        self._connection = None

    def connect(self):
        try:
            # connect to database
            # heroku
            try:
                # in your terminal, type: export DATABASE_URL="postgres://postgres:rebook2021@localhost:5432/rebook"
                DATABASE_URL = os.environ['DATABASE_URL']
                self._connection = psycopg2.connect(
                    DATABASE_URL, sslmode='require')
            # pgadmin local
            except:
                self._connection = psycopg2.connect(host='localhost', port=5432,
                                                    user='postgres', password='rebook2021', database='rebook')

            print('Connected to database...')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        self._connection.close()
        print('Disconnected from database')

    # method to create table schema
    # return True if command properly executed, False if error occurred
    def _create_tables(self):
        booklistings.create(self)
        bookbag.create(self)
        purchases.create(self)
        listingphotos.create(self)

    # helper method to execute insert, update, delete row methods
    def _execute_command(self, command, info, return_id=False):

        cursor = self._connection.cursor()

        try:
            cursor.execute(command, tuple(info))
            print("EXECUTED: " + str(command))

            # get the generated serial id back
            if return_id:
                listing_id = cursor.fetchone()[0]

        except Exception as e:
            print(str(e), file=stderr)
            return False

        cursor.close()
        self._connection.commit()
        if return_id:
            return listing_id
        else:
            return True

    # takes as input a net_id
    # returns dict with lists of active, pending, completed listing_ids
    def get_buyer_bookbag(self, net_id):
        cursor = self._connection.cursor()

        QUERY_OTHER = 'SELECT listing_id FROM bookbag ' + \
            'WHERE buyer = %s AND (listing_status = \'removed\' OR listing_status = \'taken\' OR listing_status = \'completed\')'
        QUERY_ACTIVE = 'SELECT listing_id FROM bookbag ' + \
            'WHERE buyer = %s AND listing_status = \'active\''
        QUERY_PENDING = 'SELECT listing_id FROM purchases ' + \
            'WHERE buyer = %s AND buyer_status = \'pending\''
        QUERY_COMPLETED = 'SELECT listing_id FROM purchases ' + \
            'WHERE buyer = %s AND buyer_status = \'completed\''

        cursor.execute(QUERY_OTHER, (net_id,))
        other_listings = self._get_list(cursor)

        cursor.execute(QUERY_ACTIVE, (net_id,))
        active_listings = self._get_list(cursor)

        cursor.execute(QUERY_PENDING, (net_id,))
        pending_listings = self._get_list(cursor)

        cursor.execute(QUERY_COMPLETED, (net_id,))
        completed_listings = self._get_list(cursor)

        cursor.close()

        buyer_listings = {"other": other_listings, "active": active_listings,
                          "pending": pending_listings, "completed": completed_listings}
        return buyer_listings

    # helper method for getting listing ids
    def _get_list(self, cursor):
        listings = []
        row = cursor.fetchone()
        while row:
            listings.append(row[0])
            row = cursor.fetchone()
        return listings

    # takes as input a net_id
    # returns dict with lists of active, pending, completed listing_ids
    def get_seller_station(self, net_id):
        # cursor = self._connection.cursor()

        # QUERY_ACTIVE = 'SELECT listing_id FROM booklistings ' + \
        #     'WHERE seller = %s AND seller_status = \'active\''
        # QUERY_PENDING = 'SELECT listing_id FROM booklistings ' + \
        #                 'WHERE seller = %s AND seller_status = \'pending\''
        # QUERY_COMPLETED = 'SELECT listing_id FROM booklistings ' + \
        #     'WHERE seller = %s AND seller_status = \'completed\''

        # cursor.execute(QUERY_ACTIVE, (net_id,))
        # active_listings = self._get_list(cursor)

        # cursor.execute(QUERY_PENDING, (net_id,))
        # pending_listings = self._get_list(cursor)

        # cursor.execute(QUERY_COMPLETED, (net_id,))
        # completed_listings = self._get_list(cursor)

        # cursor.close()

        active_listings = booklistings.get_active_listings(self, net_id)
        pending_listings = booklistings.get_pending_listings(self, net_id)
        completed_listings = booklistings.get_completed_listings(self, net_id)

        seller_listings = {"active": active_listings,
                           "pending": pending_listings, "completed": completed_listings}

        return seller_listings

    def _add_querystring_price(self, params, filter_price):
        query_string = ''
        if filter_price is not None:
            lower = filter_price[0]
            upper = filter_price[1]
            if lower is not None and lower != '':
                query_string += ' AND CAST(price as double precision) >= %s'
                params.append(str(lower))
            if upper is not None and upper != '':
                query_string += ' AND CAST(price as double precision) <= %s'
                params.append(str(upper))
        return query_string

    # AUTHORS ILIKE AND price AND condition AND seller_status OR AUTHORS ILIKE AND price AND condition
    def _get_querystring(self, params, filter_price, filter_condition, append_string, query, user):

        QUERY_STRING = append_string
        QUERY_STRING += self._add_querystring_price(params, filter_price)
        QUERY_STRING += ' AND seller_status = \'active\' AND NOT seller = %s'
        params.append(user)
        if filter_condition is not None:
            for i in range(len(filter_condition)):
                QUERY_STRING += ' AND condition = %s'
                params.append(filter_condition[i])
                if i + 1 < len(filter_condition):
                    QUERY_STRING += ' OR ' + append_string
                    params.append(query)
                    QUERY_STRING += self._add_querystring_price(
                        params, filter_price)
                    QUERY_STRING += ' AND seller_status = \'active\' AND NOT seller = %s'
                    params.append(user)

        return QUERY_STRING

    # takes as input an author name, cousenum, book title, isbn
    # returns list of dicts containing relevant listing info (isbn, price, condition, title, authors, coursenum, description, listing_id)
    def search(self, query, user, filter_price=None, filter_condition=None, sort=None):
        # create a cursor
        cursor = self._connection.cursor()
        querypercent = '%' + query + '%'
        params = []

        QUERY_STRING = 'SELECT listing_id ' + \
            'FROM "booklistings" WHERE '
        params.append(querypercent)
        QUERY_STRING += self._get_querystring(
            params, filter_price, filter_condition, 'authors ILIKE %s', querypercent, user)
        params.append(querypercent)
        QUERY_STRING += ' OR ' + \
            self._get_querystring(
                params, filter_price, filter_condition, 'coursenum ILIKE %s', querypercent, user)
        params.append(querypercent)
        QUERY_STRING += ' OR ' + \
            self._get_querystring(
                params, filter_price, filter_condition, 'title ILIKE %s', querypercent, user)

        try:
            queryint = int(query)
            params.append(query)
            QUERY_STRING += ' OR ' + \
                self._get_querystring(
                    params, filter_price, filter_condition, 'isbn = %s', query, user)
        except:
            pass

        if sort is None:
            QUERY_STRING += ' ORDER BY time_created DESC'
        else:
            if sort == 'price_low_to_high':
                QUERY_STRING += ' ORDER BY CAST(price AS double precision) ASC'
            elif sort == 'price_high_to_low':
                QUERY_STRING += ' ORDER BY CAST(price AS double precision) DESC'
            elif sort == 'time_most_recent':
                QUERY_STRING += ' ORDER BY time_created DESC'
            elif sort == 'time_most_old':
                QUERY_STRING += ' ORDER BY time_created ASC'

        print(QUERY_STRING)
        print(params)
        cursor.execute(QUERY_STRING, tuple(params))

        # fetch all data
        rows = []
        row = cursor.fetchone()
        while row:
            rows.append(row[0])
            row = cursor.fetchone()

        # close cursor
        cursor.close()

        return rows

# -----------------------------------------------------------------------

# For testing:


if __name__ == '__main__':

    # count = 0

    database = Database()
    database.connect()
    # print(os.environ['DATABASE_URL'])

    # generating tables
    database._create_tables()
    # count += 1

    # print(database.get_buyer(3))
    # print(database.get_buyer(7))
    # print(database.get_buyer(8))

    # books1 = database.search('', filter_price=['0', '35'])
    # for book in books1:
    #     print(book)
    # print('\n')

    # books = database.search('cos', filter_price=['', ''], filter_condition=[
    #                         None, None, None, None])
    # for book in books:
    #     print(book)

    # # insert row
    # listinginfo = ['123412542', 'clx', 'old', 131.50, 'pending', 'insert description here',
    #                'WWS315', 'computer science for nerds', 'bob', time.time()]
    # result = database.insert_row('booklistings', listinginfo)
    # print(result)
    # listinginfo = ['123412542', 'clx', 'new', 135.50, 'pending', 'insert description here',
    #                'WWS315', 'computer science for nerds', 'bob', time.time()]
    # result = database.insert_row('booklistings', listinginfo)
    # print(result)
    # userinfo = ['clx', 'Connie Xu', 'clx@princeton.edu']
    # if database.insert_row('userinfo', userinfo):
    #     count += 1
    # bookbag = ['rebook', '2', 'pending']
    # if database.insert_row('bookbag', bookbag):
    #     count += 1
    # purchases = ['1', 'clx', 'active']
    # if database.insert_row('purchases', purchases):
    #     count += 1

    # # is_in_bookbag function
    # print('is_in_bookbag: True? ' + str(database.is_in_bookbag('rebook', '2')))
    # print('is_in_bookbag: False? ' + str(database.is_in_bookbag('clx', '2')))

    # # search function
    # books = database.search('')
    # print('database.search(\'\')')
    # for book in books:
    #     print(book)
    # print('\n')
    # print(
    #     'database.search(\'123412542\', filter_price=[135, 150], sort=\'price_low_to_high\')')
    # books = database.search('123412542', filter_price=[135, 150], sort='price_low_to_high')
    # for book in books:
    #     print(book)
    # print('\n')
    # print('database.search(\'123412542\', sort=\'price_high_to_low\')')
    # books = database.search('123412542', sort='price_high_to_low')
    # for book in books:
    #     print(book)
    # print('\n')

    # print('get_listing')
    # result = database.get_listing('1')
    # print(result)

    # seller_listings = database.get_seller_station('clx')
    # print(seller_listings)

    # buyer_listings = database.get_buyer_bookbag('rebook')
    # print(buyer_listings)

    # # # update row
    # listinginfo = ['1234125', 'clx', 'new', 31.50, 'pending', 'insert descrip here',
    #                 'WWS315', 'computer science for losers', 'bob', time.time(), 1]
    # if database.update_row('booklistings', listinginfo):
    #     count += 1
    # userinfo = ['Connie Xuer', 'clx@princeton.edu', 'clx']
    # if database.update_row('userinfo', userinfo):
    #     count += 1
    # purchases = ['pending', '1']
    # if database.update_row('purchases', purchases):
    #     count += 1

    # # # delete row
    # listinginfo = ['1']
    # if database.delete_row('booklistings', listinginfo):
    #     count += 1
    # userinfo = ['clx']
    # if database.delete_row('userinfo', userinfo):
    #     count += 1
    # bookbag = ['clx', '1234125']
    # if database.delete_row('bookbag', bookbag):
    #     count += 1
    # purchases = ['1']
    # if database.delete_row('purchases', purchases):
    #     count += 1

    database.disconnect()

    # print('\n' + str(count) + "/11 commands executed!")
