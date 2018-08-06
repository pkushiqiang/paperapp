#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:27:32 2018

@author: shiqiang
"""


from domain_classes import Author, Paper

def create_author(author_id):
    return Author(author_id, "frank guo", "F. G| S.G|Shiqiang Guo")

def create_author_list():
    author_list = list()
    for author_id in range(10,15):
        author_list.append(create_author(author_id))
    return author_list

def create_paper(paper_id):
    return Paper(paper_id, "title of paper "+ str(paper_id), "1234|5678", "abstract", 2008, "venue")

def create_paper_list():
    paper_list = list()
    for paper_id in range(90,100):
        paper_list.append(create_paper(paper_id))
    return paper_list
