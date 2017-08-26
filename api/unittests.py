import unittest
import utils

class TestUtilsMethods(unittest.TestCase):

    def test_sql_connection(self):
        # tests secure sql connection
        connection = utils.get_sql_connection()
        self.assertIsNotNone(connection)


    def test_pipeline_one_data(self):
        truck_data = {
            'truck_name': 'Test Truck',
            'cuisine': 'Test Cuisine',
            'menu': [
                {
                'item_name': 'Test Item',
                'item_price': '10.00'
                },
                {
                'item_name': 'Test Item 2',
                'item_price': 10.00
                }
            ]
        }
        ids = utils.submit_new_truck(truck_data)
        menu_id = ids['menu_id']
        truck_id = ids['truck_id']
        item_ids = ids['item_ids']
        truck_name = truck_data['truck_name']
        
        # check all entries are there
        self.assertIsNotNone(truck_id)
        self.assertIsNotNone(menu_id)
        self.assertTrue(utils.entity_exists('menu_items', truck_id=truck_id))
        self.assertTrue(utils.entity_exists('menu_items', menu_id=menu_id))
        self.assertTrue(utils.entity_exists('menu_items', truck_name=truck_name))
        self.assertTrue(utils.entity_exists('truck_accounts', truck_id=truck_id))
        self.assertTrue(utils.entity_exists('truck_accounts', menu_id=menu_id))
        self.assertTrue(utils.entity_exists('truck_accounts', truck_name=truck_name))
        self.assertTrue(utils.entity_exists('truck_info', truck_id=truck_id))
        self.assertTrue(utils.entity_exists('truck_info', menu_id=menu_id))
        self.assertTrue(utils.entity_exists('truck_info', truck_name=truck_name))
        for item_id in item_ids:
            self.assertTrue(utils.entity_exists('menu_items', item_id=item_id))

        # delete this truck
        utils.delete_truck(truck_id)

        # test truck is no longer there
        self.assertIsNotNone(truck_id)
        self.assertIsNotNone(menu_id)
        self.assertFalse(utils.entity_exists('menu_items', truck_id=truck_id))
        self.assertFalse(utils.entity_exists('menu_items', menu_id=menu_id))
        self.assertFalse(utils.entity_exists('menu_items', truck_name=truck_name))
        self.assertFalse(utils.entity_exists('truck_accounts', truck_id=truck_id))
        self.assertFalse(utils.entity_exists('truck_accounts', menu_id=menu_id))
        self.assertFalse(utils.entity_exists('truck_accounts', truck_name=truck_name))
        self.assertFalse(utils.entity_exists('truck_info', truck_id=truck_id))
        self.assertFalse(utils.entity_exists('truck_info', menu_id=menu_id))
        self.assertFalse(utils.entity_exists('truck_info', truck_name=truck_name))
        for item_id in item_ids:
            self.assertFalse(utils.entity_exists('menu_items', item_id=item_id))


if __name__ == '__main__':
    unittest.main()
