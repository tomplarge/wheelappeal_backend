from flask import Flask, request
from flask_restful import Resource, Api
import os, sys, logging
import json

# self-created
import utils

# set up logging
logging.basicConfig(filename='/home/ec2-user/api.log',level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

# initialize flask app
flask_app = Flask(__name__)
flask_api = Api(flask_app)

class TruckData(Resource):
    def __init__(self):
        return

    # returns truck info table
    def get(self):
        try:
            logging.debug("Truck data request %s" % (request))
            truck_data = utils.get_full_truck_data(request.args.get('truck_id'))
            logging.debug("Trucks request returning: %s" % (truck_data))
            return truck_data
        except Exception as e:
            logging.error(e, exc_info=True)
            return "{}"

# class Menu(Resource):
#     def __init__(self):
#         return
#
#     def get(self):
#         # parse request arguments
#         # formatting: http://wheelappeal.co:5000/v1/menu?truckname=<truckname>
#         try:
#             logging.debug("Menu request: %s\nRequest arguments: %s" % (request, request.args))
#             truckname = request.args.get('truckname')
#             menu = utils.get_menu(truckname)
#             return json.dumps(menu)
#         except Exception as e:
#             logging.error(e, exc_info=True)

class Submit(Resource):
    def post(self):
        request_json = request.get_json()
        if request_json != None:
            logging.debug("Submit request: %s" % (request_json))
            utils.submit_new_truck(request_json)
        else:
            return 'Incorrect request formatting. Must be JSON.'

base_endpoint = ""
trucks_endpoint = '/truck_data'
submit_endpoint = '/submit'

flask_api.add_resource(TruckData, trucks_endpoint)
flask_api.add_resource(Submit, submit_endpoint)

if __name__ == '__main__':
    debug = os.environ.get('DEBUG')
    if debug:
        logging.debug("Flask Running in Debug Mode")
        flask_app.run(debug=True)
    else:
        flask_app.run(host="0.0.0.0")
