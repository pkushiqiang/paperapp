
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:27:32 2018

@author: shiqiang

This module test webservice API classes

"""
import os
import unittest
import pickle
from unittest.mock import MagicMock

os.environ['POSTGRES_USER'] = ""
os.environ['POSTGRES_PASSWORD'] = ""
os.environ['POSTGRES_DB'] = ""

import app
from app import  ServiceHealth, AuthorList, Authorinfo
from test_util import *
 
class TestAPIs(unittest.TestCase):
    

    def setUp(self):
        app.cache = MagicMock()
        app.dbController = MagicMock()

    def test_ServiceHealth(self):
        """
            Test ServiceHealth API.
        """
        api = ServiceHealth()
        self.assertEqual(api.get(), {'status': 'Good'})

    def test_AuthorList_not_in_cache(self):
        """
            Test AuthorList API. author list is returned by mock DB controller.
        """
        app.cache.get.return_value = None
        app.dbController.getAllAuthors.return_value = create_author_list()

        api = AuthorList()
        result = api.get()
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["id"], 10)
        self.assertEqual(result[4]["id"], 14)

    def test_AuthorInfo_in_cache(self):
        """
            Test AuthorInfo API. author info is returned by mock DB controller.
        """
        author = create_author(100)
        app.cache.get.return_value = pickle.dumps(author)
         
        api = Authorinfo()
        result = api.get(100)
        self.assertEqual(result["id"], 100)
        self.assertEqual(result["name"], "frank guo")

if __name__ == '__main__':
    unittest.main()