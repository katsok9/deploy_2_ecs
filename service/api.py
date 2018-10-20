from flask import Flask
from flask_restful import Resource, Api

from resources.deploymentList import DeploymentList
from resources.deployment import Deployment

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(Deployment, '/api/v1/deployment/deploy/<string:image>')
api.add_resource(DeploymentList, '/api/v1/deployments/')
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
