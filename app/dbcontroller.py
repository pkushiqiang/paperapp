   
    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:02:14 2018

@author: shiqiang
"""

from domain_classes import Author, Paper
import psycopg2

class DBController:

    def __init__(self, db_name, db_user, db_pass, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.conn = None

    def __del__(self ):  
        if self.conn:
            self.conn.close()
    
    def connect_to_db(self):
        if self.conn:
            self.conn.close()
        self.conn = psycopg2.connect(database = self.db_name, user = self.db_user,
                                password = self.db_pass, host = self.db_host, port = self.db_port)
 
    
    def if_table_exist(self, table_name):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM pg_catalog.pg_tables where tablename=%s", (table_name,))
        return bool(cur.rowcount)
    
    def create_tables(self):
        cur = self.conn.cursor()
        
        cur.execute("DROP TABLE IF EXISTS author_paper")
        cur.execute("DROP TABLE IF EXISTS authors")
        cur.execute("DROP TABLE IF EXISTS papers")
    
        cur.execute('''CREATE TABLE authors (
                         author_id serial PRIMARY KEY,
                         author_name VARCHAR (200),
                         aliases TEXT  
                         );''')
    
        cur.execute('''CREATE TABLE papers (
                paper_id serial PRIMARY KEY,
                title TEXT,
                author_ids TEXT,
                abstract TEXT,
                published_year smallint,
                venue VARCHAR (1000)     
                         );''')
    
        cur.execute('''CREATE TABLE author_paper (
                id serial PRIMARY KEY,
                author_id INTEGER REFERENCES authors(author_id),
                paper_id INTEGER REFERENCES papers(paper_id));''')
        cur.close()
        self.conn.commit()
        print("Table created successfully")
        
        
    def insert_author(self, author):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO authors (author_id, author_name, aliases) VALUES (%s, %s, %s)",
                       (author.author_id, author.author_name, author.aliases_str))
        self.conn.commit()
        
    def insert_paper(self, paper):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO papers (title, author_ids, abstract, published_year, venue) VALUES (%s, %s, %s, %s, %s)  RETURNING paper_id",
                    (paper.title, paper.author_ids_str, paper.abstract, paper.published_year, paper.venue))
        self.conn.commit()
        paper_id = cur.fetchone()[0]
      #  print("paper_id = ", paper_id)
        return paper_id
        
    def insert_auther_paper(self, paper, author_ids_set):
        cur = self.conn.cursor()
        author_ids = paper.author_ids_str.split("|")
        for idstr in author_ids:
            author_id = int(idstr)
            if author_id in author_ids_set:
                cur.execute("INSERT INTO author_paper (author_id, paper_id) VALUES (%s, %s)",
                                (author_id, paper.paper_id))
        self.conn.commit()        
    
    def getAuthorInfo(self, author_id):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT * FROM authors where author_id = %s", (author_id,))
            rows = cur.fetchall()
            if not rows:
                return None
        except psycopg2.DataError:
            cur.execute("ROLLBACK")
            self.conn.commit()
            return None

        row = rows[0]
        author = Author(row[0], row[1],row[2])
        author.parseAliases()
        
        cur.execute("SELECT papers.paper_id, papers.title, papers.author_ids, papers.abstract, papers.published_year, papers.venue FROM author_paper, papers WHERE author_id=%s AND author_paper.paper_id=papers.paper_id", (author_id,))
        rows = cur.fetchall()
        author.papers = list()
        for row in rows:
            paper = Paper(row[0], row[1], row[2], row[3], row[4], row[5])
            paper.parse_author_list()
            author.papers.append(paper)
        return author
    
    def getAllAuthors(self):
        authors  = list()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM authors")
        rows = cur.fetchall()
        for row in rows:
            author = Author(row[0], row[1],row[2])
            author.parseAliases()
            authors.append(author)
        return authors

        
    