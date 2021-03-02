import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from database.models import setup_db, Product, Category
from app import app

USER_TOKEN = os.environ.get('USER_TOKEN')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
DB_HOST = os.getenv('DB_HOST')  
DB_USER = os.getenv('DB_USER')  
DB_PASSWORD = os.getenv('DB_PASSWORD')  
DB_NAME = os.getenv('DB_NAME') 

class EcommerceTestCase(unittest.TestCase):
    """This class represents the ecommerce test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client 
        database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
#test get products 
    def test_get_products(self):
        res = self.client().get('/products',
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])

    def test_401_get_products_no_token(self):
        res = self.client().get('/products')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is unauthorized to make this action')

#get product by ID
        
    def test_get_product_by_id(self):
        res = self.client().get('/products/3', headers={'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['product'])

    def test_404_if_product_does_not_exist_get(self):
        res = self.client().get('/products/80', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
#get product by category ID    
    
    def test_get_products_by_category(self):
        res = self.client().get('products/category/1',
        headers = { 'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])

    def test_404_if_category_does_not_exist_get_product(self):
        res = self.client().get('/products/category/77', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

#delete product
    def test_delete_product(self):
        res = self.client().delete('/products/7', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 7)
        self.assertEqual(res.status_code, 200)
        product = Product.query.get(7)
        self.assertFalse(product)
    
    def test_404_if_product_does_not_exist_delete(self):
        res = self.client().delete('/products/110', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        
#add product
    def test_add_product_with_token(self):
        res = self.client().post('/products', json={
    "name": "Skirt",
    "description": "kiddo skirt",
    "price": '500',
    "category_id": 1
}, headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['product']['name'], 'Skirt')
        self.assertEqual(data['product']['description'], 'kiddo skirt')
        self.assertEqual(data['product']['price'], '500')
        self.assertEqual(data['product']['category_id'],1 )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_add_product_without_token(self):
        res = self.client().post('/products', json={
    "name": "Skirt",
    "description": "kiddo skirt",
    "price": '500',
    "category_id": 1
})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is unauthorized to make this action')

#edit product
    def test_edit_product_with_token(self):
        res = self.client().patch('/products/5', json={
    "name": "Blouse",
    "description": "kiddo blouse"
}, headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        product = Product.query.get(5)
        data = json.loads(res.data)
        self.assertEqual(data['product']['name'], 'Blouse')
        self.assertEqual(data['product']['description'], 'kiddo blouse')
        self.assertEqual(data['product']['price'], product.price)
        self.assertEqual(data['product']['category_id'],product.category_id )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_edit_product_without_token(self):
        res = self.client().patch('/products/5', json={
    "name": "Pants",
    "description": "kiddo pants",
})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is unauthorized to make this action')

#test get all categories
    def test_get_categories(self):
        res = self.client().get('/categories', 
        headers = {'Authorization': 'Bearer {}'.format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_401_get_categories_without_token(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is unauthorized to make this action')

#get category by ID
        
    def test_get_category_by_id(self):
        res = self.client().get('/categories/3', headers={'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])

    def test_404_if_category_does_not_exist_get(self):
        res = self.client().get('/categories/80', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

#delete category
    def test_delete_category(self):
        res = self.client().delete('/categories/5', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 5)
        self.assertEqual(res.status_code, 200)
        category = Category.query.get(5)
        self.assertFalse(category)
    
    def test_404_if_category_does_not_exist_delete(self):
        res = self.client().delete('/categories/110', 
        headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        
#add category
    def test_add_category_with_token(self):
        res = self.client().post('/categories', json={
    "type": "kids",
    "description": "Stuff for kids"
}, headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['category']['description'], 'Stuff for kids')
        self.assertEqual(data['category']['type'], 'kids')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_add_category_without_token(self):
        res = self.client().post('/categories', json={
    "type": "kids",
    "description": "Stuff for kids"
})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is unauthorized to make this action')

 
#edit category
    def test_edit_category_with_token(self):
        res = self.client().patch('/categories/1', json={
    "description": "Stuff for women"
}, headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        category = Category.query.get(1)
        data = json.loads(res.data)
        self.assertEqual(data['category']['description'],'Stuff for women')
        self.assertEqual(data['category']['type'], category.type)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_edit_category_without_token(self):
        res = self.client().patch('/categories/1', json={
    "description": "Stuff for women"
})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is unauthorized to make this action')

#RBAC Testing
    def test_add_product_ADMIN(self):
        res = self.client().post('/products', json={
    "name": "Shorts",
    "description": "shorts for all",
    "price": '500',
    "category_id": 1
}, headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['product']['name'], 'Shorts')
        self.assertEqual(data['product']['description'], 'shorts for all')
        self.assertEqual(data['product']['price'], '500')
        self.assertEqual(data['product']['category_id'], 1 )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_product_USER(self):
        res = self.client().post('/products', json={
    "name": "Skirt",
    "description": "kiddo skirt",
    "price": '500',
    "category_id": 1
}, headers = {'Authorization': 'Bearer {}'.format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_edit_category_ADMIN(self):
        res = self.client().patch('/categories/1', json={
    "description": "Stuff for babies"
}, headers = {'Authorization': 'Bearer {}'.format(ADMIN_TOKEN)})
        category = Category.query.get(1)
        data = json.loads(res.data)
        self.assertEqual(data['category']['description'],'Stuff for babies')
        self.assertEqual(data['category']['type'], category.type)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_category_USER(self):
        res = self.client().patch('/categories/1', json={
    "description": "Stuff for women"
}, headers = {'Authorization': 'Bearer {}'.format(USER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()