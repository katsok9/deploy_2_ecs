from flask_restful import Resource


def getDeploymentsList():
    return {'list of deployments': 'deployments list:'}
    pass


class DeploymentList(Resource):
    def get(self):
        return getDeploymentsList()

