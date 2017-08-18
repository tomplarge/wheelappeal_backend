import pymysql, json
import sys, os

def get_auth():
    auth = json.load(open("/home/ec2-user/db_auth.json"))
    return auth

# returns truck menu from mysql as JSON
def get_menu(truck_name):
    auth = get_auth()
    try:
        connection = pymysql.connect(host=str(auth['host']),user=str(auth['user']),passwd=str(auth['passwd']),db=str(auth['db']))
    except:
        raise Exception('Incorrect Database Authentication')

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM " + truck_name
        cursor.execute(sql)
        menu_dict = cursor.fetchall()
        return menu_dict

# submit truck data from JSON
#TODO: update table if it already exists
#TODO: don't make price int - this is on the DB side
def submit_truck(truck_data):
    auth = get_auth()
    try:
        connection = pymysql.connect(host=auth['host'],user=auth['user'],passwd=auth['passwd'],db=auth['db'])
    except:
        raise Exception('Incorrect Database Authentication')

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        print 'truck_data:',truck_data
        truck_name = truck_data['truck_name']
        cuisine = truck_data['cuisine']
        sql = 'INSERT INTO trucks (name, cuisine) VALUES ("%s", "%s")' % (truck_name, cuisine)
        cursor.execute(sql)
        sql = "CREATE TABLE %s (item varchar(30), price int(11))" % (truck_name)
        cursor.execute(sql)
        menu = truck_data['menu']
        for item in menu:
            print 'item:',item
            sql = 'INSERT INTO %s (item, price) VALUES ("%s", "%d")' % (truck_name, item['name'], int(item['price']))
            print sql
            cursor.execute(sql)
            print "executed"
            sys.__stdout__.flush()
            connection.commit()

# returns the info of all trucks as JSON
def get_trucks():
    auth = get_auth()
    try:
        connection = pymysql.connect(host=auth['host'],user=auth['user'],passwd=auth['passwd'],db=auth['db'])
    except:
        raise Exception('Incorrect Database Authentication')

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM trucks"
        cursor.execute(sql)
        truck_dict =  cursor.fetchall()
        return truck_dict

if __name__ == '__main__':
    trucks = get_trucks()
    print trucks
    for truck in trucks:
        truck_name = truck['name']
        print get_truck_menu(truck_name)
