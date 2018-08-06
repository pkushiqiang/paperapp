#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:27:32 2018

@author: shiqiang

This module will test the class DBController.

"""

import psycopg2
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from dbcontroller import DBController
from domain_classes import Author, Paper
from test_util import *

class MockConnection():
    """
        Mocked Connection class, will mocking class of psycopg2.connection.
    
    """

    def __init__(self):
        """
          the cursor instance is a MagicMock here.
        """
        self.mock_cursor = MagicMock()

    def cursor(self):
        return self.mock_cursor

    def close(self):
        print("mock connect close.")

    def commit(self):
        print("mock connect commit.")

class TestDBController(unittest.TestCase):
    
    """
       Test cases to test class DBController.
    """

    def setUp(self):
        self.dbController = DBController("db_name", "db_user", "db_pass", "db_host", 5432)
        self.mock_conn = MockConnection()
        self.dbController.conn = self.mock_conn
        self.mock_cursor = self.dbController.conn.cursor()

    def test_insert_author(self):
        """
            Test insert author.
        """
        author = create_author(123)
        self.dbController.insert_author(author)
        self.mock_cursor.execute.assert_called_with("INSERT INTO authors (author_id, author_name, aliases) VALUES (%s, %s, %s)",
                       (123, 'frank guo', 'F. G| S.G|Shiqiang Guo'))

    def test_insert_paper(self):
        """
            Test insert paper.
        """
        paper = create_paper(123)
        self.dbController.insert_paper(paper)
        self.mock_cursor.execute.assert_called_with("INSERT INTO papers (title, author_ids, abstract, published_year, venue) VALUES (%s, %s, %s, %s, %s)  RETURNING paper_id",
                    ("title of paper 123", "1234|5678", "abstract", 2008, "venue"))

    
    def test_getAuthorInfo_happycase(self):
        """
            Test get author info in happy case.
        """
        get_author_result = [(123, "frank guo", "F. G| S.G|Shiqiang Guo")]
        get_papers_result = [(1000, "title of paper 1000", "1234|5678", "abstract", 2008, "venue"),
                (1001, "title of paper 1001", "1234|5678", "abstract", 2008, "venue")]
        self.mock_cursor.fetchall.side_effect = [get_author_result, get_papers_result]
        author = self.dbController.getAuthorInfo(123)
        self.assertEqual(author.author_id, 123)
        self.assertEqual(len(author.papers), 2)
        self.assertEqual(author.papers[0].paper_id, 1000)
        self.assertEqual(author.papers[1].paper_id, 1001)

    def test_getAuthorInfo_not_found(self):
        """
            Test get author info when author is not is database.
        """
        self.mock_cursor.fetchall.side_effect = [None]
        author = self.dbController.getAuthorInfo(123)
        self.assertTrue(author is None)

    def test_getAuthorInfo_with_error(self):
        """
            Test get author info when when meets DB error.
        """
        self.mock_cursor.fetchall.side_effect = psycopg2.DataError()
        author = self.dbController.getAuthorInfo(123)
        self.mock_cursor.execute.assert_called_with("ROLLBACK")
        self.assertTrue(author is None)

    @patch('psycopg2.connect')
    def test_connect(self, connect_call):
        """
            Test coneect to database.
        """
        connect_call.return_value = self.mock_conn
        self.dbController.connect_to_db()
        connect_call.assert_called_with(database = "db_name", user = "db_user",
                                password = "db_pass", host = "db_host", port = 5432)         
        self.assertTrue(self.dbController.conn is not None)
        self.assertEqual(self.dbController.conn, self.mock_conn)

if __name__ == '__main__':
    unittest.main()