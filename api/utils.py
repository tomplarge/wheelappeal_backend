import pymysql, json

# returns truck menu from mysql as JSON
def get_menu(truck_name):

    try:
        connection = pymysql.connect( )
    except:
        raise Exception('Incorrect Info')

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM " + truck_name
        cursor.execute(sql)
        menu_dict = cursor.fetchall()
        return menu_dict

def submit_truck():
    return
    
# returns the info of all trucks as JSON
def get_trucks():

    try:
        connection = pymysql.connect( )
    except:
        raise Exception('Incorrect Info')

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
