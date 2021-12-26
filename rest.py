import json
from flask import Flask, request
from flask_restful import Resource, Api
from dbms import DBMS
from database import Database
from table import Table
import fields as my_fields
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Information Technologies Lab',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),      
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

api = Api(app)
docs = FlaskApiSpec(app)

d = DBMS()

db = d.get_or_create_database('test')
db.append_table(
    Table(
        (
            my_fields.IntegerField('id'), 
            my_fields.StringField('name'))
        ), 
        'test'
    )
db.tables['test'].add_row((1, 'testname'))
db.tables['test'].add_row((2, '2'))
db.tables['test'].add_row((3, '2'))

class DatabaseResponseSchema(Schema):
    database = fields.Dict()


class TableGetResponseSchema(Schema):
    table = fields.List(fields.Dict())


class RowResponseSchema(Schema):
    row = fields.Dict()


class PostSuccessSchema(Schema):
    message = fields.Str(default='success')


class RestDatabase(MethodResource, Resource):
    @doc(tags=['GET'])
    @marshal_with(DatabaseResponseSchema)
    def get(self, database):
        return {'database': d.get_or_create_database(database).as_dict()}

    @use_kwargs({'data': fields.List(fields.Str)})
    @doc(tags=['POST'])
    def post(self, database, data):
        new = Table.from_str_list(data)
        d.get_or_create_database(database).append_table(new)
        return {'table': str(new)}

    @doc(tags=['DELETE'])
    def delete(self, database):
        d.delete_database(database)
        return {'success': True}


class RestTable(MethodResource, Resource):
    @marshal_with(TableGetResponseSchema)
    @doc(tags=['GET'])
    def get(self, database, table):
        return {'table': d.get_or_create_database(database).tables.get(table).as_dict()}

    @use_kwargs({'data': fields.List(fields.Str)})
    @marshal_with(PostSuccessSchema)
    @doc(tags=['POST'])
    def post(self, database, table, data):
        d.get_or_create_database(database).tables.get(table).add_row(data)

    @doc(tags=['DELETE'])
    def delete(self, database, table):
        d.get_or_create_database(database).remove_table(table)


class RestRow(MethodResource, Resource):
    @marshal_with(RowResponseSchema)
    @doc(tags=['GET'])
    def get(self, database, table, id):
        return {'row': d.get_or_create_database(database).tables.get(table).get_row_as_dict(id)}
    @use_kwargs({'data': fields.List(fields.Str)})
    @doc(tags=['POST'])
    def post(self, database, table, id, data):
        print(data, flush=True)
        d.get_or_create_database(database).tables.get(table).rows[id] = data


class RestMerge(MethodResource, Resource):
    @marshal_with(TableGetResponseSchema)
    @doc(tags=['GET'])
    def get(self, database, table1, table2):
        table1 = d.get_or_create_database(database).tables.get(table1)
        table2 = d.get_or_create_database(database).tables.get(table2)
        return {'table': (table1 + table2).as_dict()}


api.add_resource(RestDatabase, '/<database>')
api.add_resource(RestTable, '/<database>/<table>')
api.add_resource(RestRow, '/<database>/<table>/<int:id>')
api.add_resource(RestMerge, '/<database>/<table1>/merge/<table2>')


docs.register(RestDatabase)
docs.register(RestTable)
docs.register(RestRow)
docs.register(RestMerge)

if __name__ == "__main__":
    app.run()
