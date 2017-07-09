import pymysql
import json

# returns truck menu from mysql as JSON
def get_truck_menu(truck_name):

    try:
        connection = pymysql.connect( host='wheelappeal.ccl05r12jihu.us-east-2.rds.amazonaws.com',user='tomplarge',passwd='Scorp714!', db='wheel_appeal_database' )
    except:
        raise Exception('Incorrect Info')

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        # Create a new record
        sql = "SELECT * FROM " + truck_name
        cursor.execute(sql)
        rows =  cursor._rows
        return rows

# returns the info of all trucks as JSON
def get_trucks():

    try:
        connection = pymysql.connect( host='wheelappeal.ccl05r12jihu.us-east-2.rds.amazonaws.com',user='tomplarge',passwd='Scorp714!', db='wheel_appeal_database' )
    except:
        raise Exception('Incorrect Info')

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        # Create a new record
        sql = "SELECT * FROM trucks"
        cursor.execute(sql)
        truck_dict =  cursor._rows
        return truck_dict

if __name__ == '__main__':
    trucks = get_trucks()
    print trucks
    for truck in trucks:
        truck_name = truck['name']
        print get_truck_menu(truck_name)
