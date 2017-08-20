import pymysql, json
import sys, os, logging


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

    return connection


# returns truck menu from mysql as JSON
def get_menu(truck_name):
    logging.info("Getting Menu for %s" % (truck_name))
    connection = get_sql_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM `%s`" % (truck_name)
        logging.debug("Executing %s" % (sql))
        try:
            cursor.execute(sql)
        except Exception as e:
            logging.error(e, exc_info=True)
            return None
        menu_dict = cursor.fetchall()
        logging.debug("Fetched menu: %s" % (menu_dict))
        return menu_dict

# submit truck data from JSON
#TODO: update table if it already exists
#TODO: don't make price int - this is on the DB side
def submit_truck(truck_data):
    logging.info("Truck submission: %s" % (json.dumps(truck_data)))
    connection = get_sql_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        truck_name = truck_data['truck_name']
        cuisine = truck_data['cuisine']

        # TODO check if entry is alrady in table
        sql = "INSERT INTO trucks (name, cuisine) VALUES ('%s', '%s')" % (truck_name, cuisine)
        logging.debug("Executing %s" % (sql))
        cursor.execute(sql)

        # TODO check if table exists
        # TODO make uuid for each truck and identify them this way
        sql = "CREATE TABLE `%s` (item varchar(30), price int(11))" % (truck_name)
        logging.debug("Executing %s" % (sql))
        cursor.execute(sql)
        menu = truck_data['menu']
        for item in menu:
            sql = "INSERT INTO `%s` (item, price) VALUES ('%s', '%d')" % (truck_name, item['name'], int(item['price']))
            logging.debug("Executing %s" % (sql))
            cursor.execute(sql)

# returns the info of all trucks as JSON
def get_trucks():
    logging.info("Retrieving trucks")
    connection = get_sql_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM trucks"
        logging.debug("Executing %s" % (sql))
        cursor.execute(sql)
        truck_dict =  cursor.fetchall()
        return truck_dict

# deletes from truck from trucks table and it's own table
def delete_truck(truck_name, connection = None):
    logging.info("Deleting truck %s" % (truck_name))
    if connection is None:
        connection = get_sql_connection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        # delete table in database
        sql = "DROP TABLE `%s`" % (truck_name)
        logging.debug("Executing %s" % (sql))
        try:
            cursor.execute(sql)
        except Exception as e:
            logging.warning(e, exc_info=True)
            logging.debug("Table %s must not exist" % (truck_name))

        # delete entry in trucks table
        sql = "DELETE FROM trucks WHERE name = '%s'" % (truck_name)
        logging.debug("Executing %s" % (sql))
        try:
            cursor.execute(sql)
        except Exception as e:
            logging.warning(e, exc_info=True)
            logging.debug("Row %s must not exist in trucks" % (truck_name))


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
        if 'test' in truck_name:
            delete_truck(truck_name, connection = connection)

    # search from tables
    with connection.cursor() as cursor:
        sql = "SHOW TABLES"
        logging.debug("Executing %s" % (sql))
        cursor.execute(sql)
        tables = cursor.fetchall()
        for (table_name,) in tables:
            if 'test' in table_name:
                delete_truck(table_name)
