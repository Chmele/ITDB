import os
from flask import Flask, request, make_response, send_file
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

    @use_kwargs({'data': fields.Dict(), 'name': fields.Str()})
    @doc(tags=['POST'])
    def post(self, database, data, name):
        new = Table.from_field_dict(data)
        d.get_or_create_database(database).append_table(new, name)
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
        d.get_or_create_database(database).tables.get(table).rows[id] = data


class RestMerge(MethodResource, Resource):
    @marshal_with(TableGetResponseSchema)
    @doc(tags=['GET'])
    def get(self, database, table1, table2):
        table1 = d.get_or_create_database(database).tables.get(table1)
        table2 = d.get_or_create_database(database).tables.get(table2)
        return {'table': (table1 + table2).as_dict()}


class RestCol(MethodResource, Resource):
    @doc(tags=['GET'])
    def get(self, database, table, row, field):
        table = d.get_or_create_database(database).tables.get(table)
        value = table.as_dict()[row][field]
        field = list(filter(lambda f: f.name == field, table.fields))[0]
        if isinstance(field, my_fields.PngField):
            response = send_file(
                path_or_file=rf"C:\Users\admin\Desktop\myDB\pictures\{value}",
                mimetype="application/octet-stream",
                as_attachment=True,
                download_name=value
            )
            return response
        else:
            return value
    # @doc(tags=['POST'])
    # @use_kwargs({'data': fields.})
    # def post(self, database, table, row, field, data):
    #     image_file = data
    #     image_file.save(rf"C:\Users\admin\Desktop\myDB\pictures\{'current'}")
        

@app.route("/<database>/<table>/<int:row>/<field>", methods=["POST"])
def post_file(database, table, row, field):
    """Upload a file."""

    with open(os.path.join(r"C:\Users\admin\Desktop\myDB\pictures", 'test2.png'), "wb") as fp:
        fp.write(request.data)
        d.get_or_create_database(database).tables.get(table).rows[row][0] = 'test2.png'
        return ""


api.add_resource(RestDatabase, '/<database>')
api.add_resource(RestTable, '/<database>/<table>')
api.add_resource(RestRow, '/<database>/<table>/<int:id>')
api.add_resource(RestMerge, '/<database>/<table1>/merge/<table2>')
api.add_resource(RestCol, '/<database>/<table>/<int:row>/<field>')


docs.register(RestDatabase)
docs.register(RestTable)
docs.register(RestRow)
docs.register(RestMerge)
docs.register(RestCol)

if __name__ == "__main__":
    app.run()
