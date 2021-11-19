from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from run_services import run_services


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version='0.0',
          title='Solai services API',
          description='RESTful API for controlling your Solai services')

ns = api.namespace('services', description='services operations')

service_model = api.model('services', {
    'name': fields.String(required=True, description='service name'),
    'status': fields.String(required=True, description='on or off'),
    'pid': fields.Integer(required=False, default=0, readonly=True, description='pid of script running on server')
})


class ServiceUtil(object):
    def __init__(self):
        self.services = []

    def get(self, name):
        for service in self.services:
            if service['name'] == name:
                return service
        api.abort(404, f"service {name} does not exist.")

    def create(self, data):
        service = data
        self.services.append(service)

        self.services = run_services(self.services)

        return service

    def update(self, name, data):
        service = self.get(name)
        service.update(data)

        self.services = run_services(self.services)

        return self.get(name)

    def delete(self, name):
        service = self.get(name)
        self.services.remove(service)

        self.services = run_services(self.services)

@ns.route('/')
class ServiceList(Resource):
    """Shows a list of all services, and lets you POST to add new services"""

    @ns.marshal_list_with(service_model)
    def get(self):
        """List all services"""
        return service_util.services

    @ns.expect(service_model)
    @ns.marshal_with(service_model, code=201)
    def post(self):
        """Create a new service"""
        return service_util.create(api.payload)


@ns.route('/<name>')
@ns.response(404, 'service not found')
@ns.param('name', 'The service identifier')
class Service(Resource):
    """Show a single service item and lets you update/delete them"""

    @ns.marshal_with(service_model)
    def get(self, name):
        """Fetch a service given its resource identifier"""
        return service_util.get(name)

    @ns.response(204, 'service deleted')
    def delete(self, name):
        """Delete a service given its identifier"""
        service_util.delete(name)
        return '', 204

    @ns.expect(service_model, validate=True)
    @ns.marshal_with(service_model)
    def put(self, name):
        """Update a service given its identifier"""
        return service_util.update(name, api.payload)
    
    @ns.expect(service_model)
    @ns.marshal_with(service_model)
    def patch(self, name):
        """Partially update a service given its identifier"""
        return service_util.update(name, api.payload)


service_util = ServiceUtil()
service_util.create({'name': 'autocharge', 'status': 'off', 'pid': 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)