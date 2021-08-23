#!/usr/bin/env python

# -----------------------------------------------------------------------
# user.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------

class User:

    def __init__(self, name, netid, email):
        self._name = name
        self._netid = netid
        self._email = email.lower()

    def __str__(self):
        name = 'name: ' + self._name
        netid = 'netid: ' + self._netid
        email = 'email: ' + self._email

        info = [name, netid, email]

        return '\n'.join(info)

    def getName(self):
        return self._name

    def getNetID(self):
        return self._netid

    def getEmail(self):
        return self._email
