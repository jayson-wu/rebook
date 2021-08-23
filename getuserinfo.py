#!/usr/bin/env python

# -----------------------------------------------------------------------
# getuserinfo.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------

from req_lib import ReqLib
from sys import argv, stderr
from user import User

'''
This endpoint returns information about
a user within the Princeton community.
This endpoint provides
a bit less information than does the 
endpoint in the file users.py.
The only parameter that the endpoint requires
is the user's netid. The parameter's name is:
uid
The return value has the following information
about the user:
displayname (Full name of the user)
universityid (PUID number)
mail (user's email address)
'''

# takes in a netid and retrieves displayname, universityid, mail address


def getUserInfo(netid):
    req_lib = ReqLib()

    req = req_lib.getJSON(
        req_lib.configs.USERS_BASIC,
        uid=netid,
    )
    if req == []:
        return User('rebook', 'rebook', 'princetonrebook@gmail.com')
    # print(req)
    info = req[0]
    netid = info['uid']
    name = info['displayname']
    # email = info['mail']
    if 'mail' in info:
        email = info['mail']
    else:
        print("No email found!", file=stderr)

    user = User(name, netid, email)

    return user


# takes in uid from command line, and tests getUserInfo


def main(argv):
    uid = argv[1]
    print(getUserInfo(uid))


if __name__ == "__main__":
    main(argv)
