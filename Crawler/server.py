from flask import Flask
from flask_restful import Api, Resource
from query import main, statistics_by_id

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


class Statistics(Resource):
    def get(self, id):
        statistics = statistics_by_id(id)

        response = app.response_class(
            response=statistics,
            status=200,
            mimetype='application/json'
        )
        return response


api.add_resource(Statistics, "/statistics/<string:id>")

app.run(port=3000)
