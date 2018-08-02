#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:44:08 2018

@author: shiqiang
"""

class Author :
    def __init__(self, author_id, author_name, aliases_str):
        self.author_id = author_id
        self.author_name = author_name
        self.aliases_str = aliases_str
       
    def parseAliases(self):
        self.aliases  = self.aliases_str.split('|')
        
    def __str__(self):
        return (str(self.author_id) + ', ' + self.author_name + ', ' + self.aliases_str[:30] + '...' + '\n')
    
    
class Paper :
    def __init__(self, paper_id, title, author_ids_str, abstract, published_year, venue):
        self.paper_id = paper_id
        self.title = title
        self.author_ids_str = author_ids_str
        self.abstract = abstract
        self.published_year = published_year
        self.venue = venue
        
    def parse_author_list(self):
        self.author_ids = self.author_ids_str.split('|')
        
    def __str__(self):
        return (str(self.paper_id) + ', ' + self.title + ', ' + str(self.published_year)  + ', '+  self.venue + '\n')