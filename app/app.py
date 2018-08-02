#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:27:32 2018

@author: shiqiang
"""
from flask import Flask
from flask_restful import abort, Api, Resource
from flask_restful import fields, marshal_with
from dbcontroller import DBController
import subprocess, time

app = Flask(__name__)
api = Api(app)

dbController = DBController()

author_list_fields = {
    'id':   fields.Integer(attribute='author_id'),
    'name': fields.String(attribute='author_name'),
    'aliases': fields.List(fields.String)
}

paper_list_fields = {
    'paper_id': fields.Integer,
    'title': fields.String,
    'author_ids': fields.List(fields.String),
    'published_year': fields.Integer(),
    'venue': fields.String()    
}

author_info_field = author_list_fields.copy()
author_info_field['papers'] = fields.List(fields.Nested(paper_list_fields))

def abort_if_author_doesnt_exist(author_id):
    abort(404, message="author {} doesn't exist".format(author_id))
    
def abort_if_author_id_is_invalid(author_id):
    try:
        int(author_id)
    except ValueError:
        abort(404, message="author id {} doesn't exist".format(author_id))
    

class ServiceHealth(Resource):
    def get(self):
        return {'status': 'Good'}
    
class AuthorList(Resource):
    @marshal_with(author_list_fields)
    def get(self):
        return dbController.getAllAuthors()
    
class Authorinfo(Resource):
    @marshal_with(author_info_field)
    def get(self, author_id):
        abort_if_author_id_is_invalid(author_id)
        author = dbController.getAuthorInfo(author_id)
        if not author:
            abort_if_author_doesnt_exist(author_id)
        return author

##
## Actually setup the Api resource routing here
##
api.add_resource(ServiceHealth, '/')
api.add_resource(AuthorList, '/authors')
api.add_resource(Authorinfo, '/authorinfo/<author_id>')

def wait_for_db_server():
    connected = False
    while not connected:
        try:
            dbController.connect()
            connected = True
        except Exception as err:
            print("Connect DB met error", err)
            print("Cannot connect to db, will retry later...\n")
            time.sleep(5)

    print("DB server is started, continue...")

def backfill_if_necessary():
    if not dbController.if_table_exist('authors'):
        print("Table [authors] is not exist, will backfill the data..")
        subprocess.run(["./backfill.sh"])

def main():
    wait_for_db_server()
    backfill_if_necessary()
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':main()
