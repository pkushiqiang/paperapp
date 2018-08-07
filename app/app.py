#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:27:32 2018

@author: shiqiang

This module define the webservices API, and instance.
"""

import os
from flask import Flask
from flask_restful import abort, Api, Resource
from flask_restful import fields, marshal_with
from dbcontroller import DBController
import subprocess, time, sys
import pickle
import redis

CACHE_TTL_SECONDS = 60

app = Flask(__name__)
api = Api(app)

# Get DB configurations.
DB_HOST='db'
DB_USER=os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']
DB_NAME = os.environ['POSTGRES_DB']
DB_PORT = '5432'

dbController = DBController(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)
cache = redis.Redis(host='paper_cache', port=6379)


"""
Define how to render Author instance.
"""
author_list_fields = {
    'id':   fields.Integer(attribute='author_id'),
    'name': fields.String(attribute='author_name'),
    'aliases': fields.List(fields.String)
}

"""
Define how to render Paper instance.
"""
paper_list_fields = {
    'paper_id': fields.Integer,
    'title': fields.String,
    'author_ids': fields.List(fields.String),
    'published_year': fields.Integer(),
    'venue': fields.String()    
}

"""
Define how to render autor info  instance.
"""
author_info_field = author_list_fields.copy()
author_info_field['papers'] = fields.List(fields.Nested(paper_list_fields))

def abort_if_author_doesnt_exist(author_id):
    """
        Return HTTP 404 when author is not in DB.
    """
    abort(404, message="author {} doesn't exist".format(author_id))
    
def abort_if_author_id_is_invalid(author_id):
    """
        Return HTTP 404 when author id is not valid, like it's not digit.
    """
    try:
        int(author_id)
    except ValueError:
        abort(404, message="author id {} doesn't exist".format(author_id))

def set_to_cache(key, obj):
    """
        Serailize object, and ersist it in Redis with TTL.
    """
    pickled_object = pickle.dumps(obj)
    cache.setex(key, pickle.dumps(obj), CACHE_TTL_SECONDS)

def get_from_cache(key):
    """
        Get object from Redis, and Deserailize it.
    """
    pickled_object = cache.get(key)
    if pickled_object is not None:
        obj = pickle.loads(pickled_object)
        print("key [{}] hit the cache!".format(key), file=sys.stderr)
        return obj
    else:
        print("key [{}] isn't in the cache.".format(key), file=sys.stderr) 

class ServiceHealth(Resource):
    """
       API show if the service is running.
    """
    def get(self):
        return {"status": "Good"}
    
class AuthorList(Resource):
    """
       API return author list.
    """
    @marshal_with(author_list_fields)
    def get(self):
        key = 'author_list'
        author_list = get_from_cache(key)
        if author_list is None:
            author_list = dbController.getAllAuthors()
            set_to_cache(key, author_list)
        return author_list
    
class Authorinfo(Resource):
    """
       API return author info, include all his papers.
    """
    @marshal_with(author_info_field)
    def get(self, author_id):
        abort_if_author_id_is_invalid(author_id)
        key = 'authorinfo_' + str(author_id)
        author = get_from_cache(key)
        if author is None:
            author = dbController.getAuthorInfo(author_id)
            if not author:
                abort_if_author_doesnt_exist(key)
            set_to_cache(key, author)
        return author

##
## Setup the Api resource routing here
##
api.add_resource(ServiceHealth, '/')
api.add_resource(AuthorList, '/authors')
api.add_resource(Authorinfo, '/authorinfo/<author_id>')

def wait_for_db_server():
    """
       Loop try to connect to DB.
    """
    connected = False
    while not connected:
        try:
            dbController.connect_to_db()
            connected = True
        except Exception as err:
            print("Cannot connect to db, will retry later...\n", file=sys.stderr)
            time.sleep(5)

    print("DB server is started, continue start the service...", file=sys.stderr)

def backfill_if_necessary():
    """
       If the author table is not in DB, call backfill script.
    """
    if not dbController.if_table_exist('authors'):
        print("Table [authors] is not exist, will backfill the data..")
        subprocess.run(["./backfill.sh"])

def main():
    wait_for_db_server()
    backfill_if_necessary()
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':main()
