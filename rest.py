import json
from flask import Flask, request
from flask_restful import Resource, Api
from dbms import DBMS
from database import Database
from table import Table
from fields import *


app = Flask(__name__)
api = Api(app)

d = DBMS()

db = d.get_or_create_database('test')
db.append_table(Table((IntegerField('id'), StringField('name'))), 'test')
db.tables['test'].add_row((1, 'testname'))
db.tables['test'].add_row((2, '2'))
db.tables['test'].add_row((3, '2'))

class RestDatabase(Resource):
    def get(self, database):
        return {database: d.get_or_create_database(database).as_dict()}

class RestTable(Resource):
    def get(self, database, table):
        return {table: d.get_or_create_database(database).tables.get(table).as_dict()}
    
    def post(self, database, table):
        data = json.loads(request.form['data'])
        d.get_or_create_database(database).tables.get(table).add_row(data)

class RestRow(Resource):
    def get(self, database, table, id):
        return {"row": d.get_or_create_database(database).tables.get(table).get_row_as_dict(id)}

api.add_resource(RestDatabase, '/<database>')
api.add_resource(RestTable, '/<database>/<table>')
api.add_resource(RestRow, '/<database>/<table>/<int:id>')

if __name__ == "__main__":
    app.run()