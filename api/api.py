from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os, sys

# self-created
import utils

flask_app = Flask(__name__)
flask_api = Api(flask_app)

class Trucks(Resource):
    def __init__(self):
        return

    def get(self):
        trucks = utils.get_trucks()
        return jsonify(trucks)

class Menu(Resource):
    def __init__(self):
        return
    def get(self):
        # parse request arguments
        # formatting: http://wheelappeal.co:5000/v1/menu?truckname=<truckname>
        try:
            truckname = request.args.get('truckname')
            menu = utils.get_menu(truckname)
            return menu
        except:
            return 'Incorrect request formatting'

class Submit(Resource):
    def post(self):
        request_json = request.get_json()
        if request_json != None:
            print 'request:',request_json
            utils.submit_truck(request_json)
        else:
            return 'Incorrect request formatting. Must be JSON.'

base_endpoint = "/v1"
trucks_endpoint = '/'.join((base_endpoint, "trucks"))
menu_endpoint = '/'.join((base_endpoint, 'menu'))
submit_endpoint = '/'.join((base_endpoint, 'submit'))
flask_api.add_resource(Menu, menu_endpoint)
flask_api.add_resource(Trucks, trucks_endpoint)
flask_api.add_resource(Submit, submit_endpoint)

if __name__ == '__main__':
    debug = os.environ.get('DEBUG')
    if debug:
        print 'Debug Mode'
        flask_app.run(debug=True)
    else:
        flask_app.run(host="0.0.0.0")
