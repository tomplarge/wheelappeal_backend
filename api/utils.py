import pymysql, json
import sys, os, logging
import uuid
from passlib.hash import argon2

#TODO truck_id and menu_id can start with 't' or 'm'
################################################################################
############################## Executive #######################################
################################################################################

def create_db_from_scratch():
    # create truck_accounts table
    sql = "CREATE TABLE truck_accounts (\
            truck_id char(37) NOT NULL,\
            truck_name varchar(30) NOT NULL,\
            menu_id char(37) NOT NULL,\
            pw_hash char(73) NOT NULL,\
            CONSTRAINT truck_accounts_pk PRIMARY KEY (truck_id, menu_id))"
    execute_sql(sql)

    # create truck_info table
    sql = "CREATE TABLE truck_info (\
            truck_name varchar(30) NOT NULL,\
            cuisine varchar(30) NOT NULL,\
            truck_id char(37) NOT NULL,\
            menu_id char(37) NOT NULL,\
            CONSTRAINT truck_info_pk PRIMARY KEY (truck_id, menu_id),\
            CONSTRAINT truck_info_fk FOREIGN KEY (truck_id) REFERENCES truck_accounts(truck_id))"
    execute_sql(sql)

    # create menu_items table
    sql = "CREATE TABLE menu_items (\
            truck_id char(37) NOT NULL,\
            menu_id char(37) NOT NULL,\
            item_id char(37) NOT NULL,\
            truck_name varchar(30) NOT NULL,\
            item_name varchar(50) NOT NULL,\
            item_price decimal(4,2) NOT NULL,\
            CONSTRAINT menu_items_pk PRIMARY KEY (truck_id, menu_id, item_id),\
            CONSTRAINT menu_items_fk FOREIGN KEY (truck_id) REFERENCES truck_accounts(truck_id))"
    execute_sql(sql)


# executes sql statement, logging as it goes
def execute_sql(sql_string,connection=None):
    if connection is None:
        connection = get_sql_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        logging.debug("Executing %s" % (sql_string))
        try:
            cursor.execute(sql_string)
        except Exception as e:
            logging.error(e, exc_info=True)
            return None

    return cursor.fetchall()


def get_auth():
    auth = json.load(open("/home/ec2-user/db_auth.json"))
    return auth


def get_sql_connection():
    auth = get_auth()
    try:
        connection = pymysql.connect(
        host=str(auth['host']),
        user=str(auth['user']),
        passwd=str(auth['passwd']),
        db=str(auth['db']),
        autocommit=True)
    except Exception as e:
        logging.error(e, exc_info=True)
        return None

    return connection

#TODO: fix this
def clean_db():
    """
    Cleans database by:
    1. Getting rid of trucks with 'test' in the name
    2. Getting rid of trucks with no menu
    """
    logging.info("Cleaning wheel_appeal_database")
    connection = get_sql_connection()
    trucks = get_trucks()

    # search the trucks table
    for truck in trucks:
        truck_name = truck['name']

        # if truck name has 'test' in it
        if 'test' in truck_name.lower():
            delete_truck(truck_name, connection = connection)

    # search from tables
    with connection.cursor() as cursor:
        sql = "SHOW TABLES"
        tables = execute_sql(sql)
        for (table_name,) in tables:
            if table_name == 'trucks':
                continue
            if 'test' in table_name:
                delete_truck(table_name)
            menu = get_menu(table_name)
            logging.debug(menu)

################################################################################
############################## API-Related #####################################
################################################################################

# Returns boolean whether truck exists in specified table
def entity_exists(table, truck_id = None, menu_id = None, item_id = None, truck_name = None):
    if truck_id is not None:
        sql = "SELECT * FROM %s WHERE truck_id = '%s'" % (table, truck_id)
    elif menu_id is not None:
        sql = "SELECT * FROM %s WHERE menu_id= '%s'" % (table, menu_id)
    elif item_id is not None:
        sql = "SELECT * FROM menu_items WHERE item_id= '%s'" % (item_id)
    elif truck_name is not None:
        sql = "SELECT * FROM %s WHERE truck_name = '%s'" % (table, truck_name)
    else:
        raise Exception('Must provide either truck_id or truck_name')
    entries = execute_sql(sql)
    if len(entries) == 0:
        return False
    else:
        return True


# returns truck menu from mysql as JSON
def get_menu(ID):
    # if truck id
    print ID
    if ID[0] == 't':
        logging.info("Retrieving menu for truck_id %s" % (ID))
        sql = "SELECT item_name, item_price FROM menu_items WHERE truck_id = '%s'" % (ID)
    elif ID[0] == 'm':
        logging.info("Retrieving menu for menu_id %s" % (ID))
        sql = "SELECT item_name, item_price FROM menu_items WHERE menu_id = '%s'" % (ID)
    else:
        raise Exception("Incorrectly formatted ID")
    menu = execute_sql(sql)

    # convert decimals to strings
    for entry in menu:
        entry['item_price'] = str(entry['item_price'])

    return menu

# returns the info of all trucks as JSON.
# If truck_name or truck_id provided, then return info only for that truck
def get_truck_info(truck_id = None):
    if truck_id is not None:
        logging.info("Retrieving truck info for truck_id %s" % (truck_id))
        sql = "SELECT * FROM truck_info WHERE truck_id = '%s'" % (truck_id)
    else:
        logging.info("Retrieving all truck info")
        sql = "SELECT * FROM truck_info"
    truck_info = execute_sql(sql)

    return truck_info

def get_full_truck_data(truck_id = None):
    truck_info = get_truck_info(truck_id)
    truck_data = []
    for truck_json in truck_info:
        truck_id = truck_json['truck_id']
        menu = get_menu(truck_id)
        truck_json['menu'] = menu
        truck_data.append(truck_json)

    return truck_data


# submit new truck data from JSON. Returns truck_id and menu_id
def submit_new_truck(truck_data):
    """
    truck_data = {
        'truck_name': (string),
        'cuisine': (string),
        'menu': [
            {
            'name': (string),
            'price': (int/string)
            },
            ...
        ]
    }
    """

    logging.info("Truck submission: %s" % (json.dumps(truck_data)))
    truck_name = truck_data['truck_name']
    cuisine = truck_data['cuisine']
    truck_id = 't' + str(uuid.uuid4())
    menu_id = 'm' + str(uuid.uuid4())
    pw_hash = argon2.hash("password") # TODO: make this real!

    # insert into truck_accounts
    sql = "INSERT INTO truck_accounts (truck_id, truck_name, menu_id, pw_hash)\
            VALUES ('%s','%s','%s','%s')" % (truck_id, truck_name, menu_id, pw_hash)
    execute_sql(sql)

    # insert into truck_info
    sql = "INSERT INTO truck_info (truck_id, menu_id, truck_name, cuisine)\
            VALUES ('%s','%s','%s','%s')" % (truck_id, menu_id, truck_name, cuisine)
    execute_sql(sql)

    # parse and insert menu
    menu = truck_data['menu']
    item_ids = []
    for item in menu:
        #TODO this allows for the same item to be added twice. perhaps hash it for id
        item_id = 'i' + str(uuid.uuid4())
        item_ids.append(item_id)
        sql = "INSERT INTO menu_items (menu_id, truck_id, item_id, item_name, item_price, truck_name)\
                VALUES ('%s','%s','%s','%s','%s','%s')" % (menu_id, truck_id, item_id, item['item_name'], item['item_price'], truck_name)
        execute_sql(sql)

    return {'truck_id': truck_id, 'menu_id': menu_id, 'item_ids': item_ids}


# deletes from truck from all tables
def delete_truck(truck_id):
    logging.info("Deleting truck %s" % (truck_id))

    # delete from truck_info
    sql = "DELETE FROM truck_info WHERE truck_id = '%s'" % (truck_id)
    execute_sql(sql)

    # delete from menu_items
    sql = "DELETE FROM menu_items WHERE truck_id = '%s'" % (truck_id)
    execute_sql(sql)

    # delete from truck_accounts
    sql = "DELETE FROM truck_accounts WHERE truck_id = '%s'" % (truck_id)
    execute_sql(sql)
