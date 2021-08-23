#!/usr/bin/env python

# -----------------------------------------------------------------------
# book.py
# Author: Sophie Li, Jayson Wu, Connie Xu
# -----------------------------------------------------------------------

class Book:

    def __init__(self, isbn, title, subtitle, authors, publisher, publishedDate, description, image, retailPrice):
        self._isbn = isbn
        self._title = title
        self._subtitle = subtitle
        self._authors = authors
        self._publisher = publisher
        self._publishedDate = publishedDate
        self._description = description
        self._image = image
        self._retailPrice = retailPrice

    def __str__(self):
        isbn = 'isbn: ' + self._isbn
        title = 'title: ' + self._title
        subtitle = 'subtitle: ' + self._subtitle
        authors = 'authors: '
        for author in self._authors:
            authors += author + ', '
        authors = authors[:-2]
        publisher = 'publisher: ' + self._publisher
        publishedDate = 'published date: ' + self._publishedDate
        description = 'description: ' + self._description
        image = 'image: ' + self._image
        retailPrice = 'retail price: ' + self._retailPrice

        info = [isbn, title, subtitle, authors,
                publisher, publishedDate, description, image, retailPrice]

        strInfo = '\n'.join(info)

        return strInfo

    def getAuthorString(self):
        authors = ''
        for author in self._authors:
            authors += author + ', '
        authors = authors[:-2]
        return authors

    def getISBN(self):
        return self._isbn

    def getTitle(self):
        return self._title

    def getSubtitle(self):
        return self._subtitle

    def getAuthors(self):
        return self._authors

    def getPublisher(self):
        return self._publisher

    def getPublishedDate(self):
        return self._publishedDate

    def getDescription(self):
        return self._description

    def getImage(self):
        return self._image

    def getRetailPrice(self):
        return self._retailPrice