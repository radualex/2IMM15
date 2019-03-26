from flask import Flask
from flask_restful import Api, Resource
from query import main

app = Flask(__name__)
api = Api(app)


class Query(Resource):
    def get(self, query):
        videos = main(query)

        response = app.response_class(
            response=videos,
            status=200,
            mimetype='application/json'
        )
        return response


api.add_resource(Query, "/query/<string:query>")

app.run(port=3000)
