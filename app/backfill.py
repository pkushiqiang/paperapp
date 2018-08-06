#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:27:32 2018

@author: shiqiang

The module implements backfill the tables from CSV files.

"""
import os
import csv
from domain_classes import Author, Paper
from dbcontroller import DBController


AUTHORS_CSV_FILE = 'authors.csv'
PAPERS_CSV_FILE = 'papers.csv'
author_ids_set = set()

DB_HOST='db'
DB_USER =  os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']
DB_NAME = os.environ['POSTGRES_DB']
DB_PORT = '5432'

dbController = DBController(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)
dbController.connect_to_db()

def backfill_authors():
    """
        Backfill authors into author table. 
    """
    with open(AUTHORS_CSV_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                author = Author(int(row[0]), row[1], row[2])
             #   print(author)
                dbController.insert_author(author)
                author_ids_set.add(author.author_id)
            line_count += 1
        print(f'Processed {line_count} lines.')


def backfill_good_papers():
    """
        Backfill papers into paper table. Ignore lines with format error.
        Insert the autor paper relationship into author-paper table.
    """
    with open(PAPERS_CSV_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                try:
                    paper = Paper(None, row[0], row[1], row[2], int(row[3]), row[4])
             #       print(paper)
                    paper_id = dbController.insert_paper(paper)
                    paper.paper_id = paper_id
                    dbController.insert_auther_paper(paper, author_ids_set)
                except  ValueError:  
                    print("Meet csv format error in line: ", str(line_count), "\n")
                    
            line_count += 1
        print(f'Processed {line_count} lines.')

        
def main():
    print("Create tables in db ...")
    global dbController
    try:
        dbController.create_tables()
        print("Loading data to db ...")
        backfill_authors()
        backfill_good_papers()     
    finally:
        if dbController.conn:
            dbController.conn.close()

if __name__ == "__main__": main()