import os
from flask import Flask, request, jsonify, abort, redirect, url_for, session, render_template

from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db, Product, Category, db
from controllers.auth import AuthError, requires_auth
import sys
from functools import wraps
import json
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv

from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import traceback



app = Flask(__name__)
setup_db(app)
CORS(app)
oauth = OAuth(app)


#getting Auth variables
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'ecommerce1987.us.auth0.com')
AUTH0_JWT_API_AUDIENCE = os.environ.get('AUTH0_JWT_API_AUDIENCE', 'http://localhost:5000')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID', 'GXZmKC2JpsM8XYSFpMTv0dYQ8gvSLtnZ')
AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL', 'https://ecommerce-api-udacity.herokuapp.com/callback')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET','l26eCs8Gnqlb07DoQsTMaH3z8j3WZ1N2P1NZ3h9yeL1H4vA2y6VnvIV0LZAItIIy')



## APIs

#get all products

@app.route('/products')
@requires_auth('get:products')
def get_products(token):
    try:
        all = Product.query.order_by('id').all()
        products = [product.format() for product in all]
        return jsonify({
  'success': True,
  'products': products
}), 200
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(400)
    finally:
      db.session.close()

#add product

@app.route('/products', methods=['POST'])
@requires_auth('post:products')
def add_product(token):
    data = request.get_json()
    try: 
        product = Product(name=data.get('name'), 
        description=data.get('description'),  
        price=data.get('price'),
        category_id=data.get('category_id')
         )
        product.insert()
        return jsonify({
            'success': True,
            'product': product.format()
        }),200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()
#get product by category ID

@app.route('/products/category/<int:category_id>', methods=['GET'])
@requires_auth('get:products/category')
def get_product_by_category(token, category_id):
    data = request.get_json()
    all = Product.query.filter(Product.category_id == category_id).order_by('id').all()
    if not all:
        abort(404)
    try:
        products = [product.format() for product in all]
        return jsonify({
            'success': True,
            'products': products
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()

#get product by ID
@app.route('/products/<int:id>', methods=['GET'])
@requires_auth('get:products')
def get_product(token, id):
    data = request.get_json()
    product = Product.query.filter(Product.id == id).one_or_none()
    if not product:
        abort(404)
    try:
        return jsonify({
            'success': True,
            'product': [product.format()]
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()

#edit product
@app.route('/products/<int:id>', methods=['PATCH'])
@requires_auth('patch:products')
def edit_product(token, id):
    data = request.get_json()
    product = Product.query.filter(Product.id == id).one_or_none()
    if not product:
        abort(404)
    try:
        if data.get('name'):
            name = data.get('name') 
            product.name = name
        if data.get('description'):
            description = data.get('description') 
            product.description = description
        if data.get('price'):
            price = data.get('price') 
            product.price = price
        if data.get('category_id'):
            category_id = data.get('category_id') 
            product.category_id = category_id
        product.update()
        return jsonify({
            'success': True,
            'product': product.format()
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()
#delete product

@app.route('/products/<int:id>', methods=['DELETE'])
@requires_auth('delete:products')
def delete_product(token, id):
    product = Product.query.filter(Product.id == id).one_or_none()
    if not product:
        abort(404)
    try:
        product.delete()
        return jsonify({
            'success': True,
            "delete": id
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()

#get all categories

@app.route('/categories')
@requires_auth('get:categories')
def get_categories(token):
    try:
        all = Category.query.order_by('id').all()
        categories = [category.format() for category in all]
        return jsonify({
  'success': True,
  'categories': categories
}), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(400)
    finally:
      db.session.close()

#add category

@app.route('/categories', methods=['POST'])
@requires_auth('post:categories')
def add_category(token):
    data = request.get_json()
    try: 
        category = Category(type=data.get('type'), description=data.get('description'))
        category.insert()
        return jsonify({
            'success': True,
            'category': category.format()
        }),200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()

#edit category
@app.route('/categories/<int:id>', methods=['PATCH'])
@requires_auth('patch:categories')
def edit_category(token, id):
    data = request.get_json()
    category = Category.query.filter(Category.id == id).one_or_none()
    if not category:
        abort(404)
    try:
        if data.get('type'):
            type = data.get('type') 
            category.type = type
        if data.get('description'):
            description = data.get('description') 
            category.description = description
        category.update()
        return jsonify({
            'success': True,
            'category': category.format()
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()
#delete category

@app.route('/categories/<int:id>', methods=['DELETE'])
@requires_auth('delete:categories')
def delete_category(token, id):
    category = Category.query.filter(Category.id == id).one_or_none()
    if not category:
        abort(404)
    try:
        category.delete()
        return jsonify({
            'success': True,
            "delete": id
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()

#get category by ID
@app.route('/categories/<int:id>', methods=['GET'])
@requires_auth('get:categories')
def get_category(token, id):
    data = request.get_json()
    category = Category.query.filter(Category.id == id).one_or_none()
    if not category:
        abort(404)
    try:
        return jsonify({
            'success': True,
            'category': [category.format()]
        }), 200
    except:
        print(sys.exc_info())
        db.session.rollback()
        abort(401)
    finally:
      db.session.close()

#Generate an authorization URL
@app.route("/authorization/url", methods=["GET"])
def generate_auth_url():
    url = f'https://{AUTH0_DOMAIN}/authorize' \
        f'?audience={AUTH0_JWT_API_AUDIENCE}' \
        f'&response_type=token&client_id=' \
        f'{AUTH0_CLIENT_ID}&redirect_uri=' \
        f'{AUTH0_CALLBACK_URL}'
        
    return jsonify({
        'url': url
    })

@app.route('/callback', methods=['GET'])
def callback_handling():
    try:
        auth = oauth.authorize_access_token()
        user = oauth.get('userinfo')
        userinfo = user.json()
        # store jwt in session
        session['token'] = auth['access_token']
         # store username in session
        session['user'] = userinfo['name']
    except Exception as e:    
        print('Error on callback:', e)    
        traceback.print_exc()


#error handlers 
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "User is unauthorized to make this action"
        }), 401

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unable to process the contained instructions"
        }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "The server cannot or will not process the request due to something that is perceived to be a client error"
        }), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "The server encountered an unexpected condition that prevented it from fulfilling the request"
        }), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
        }), 405


@app.errorhandler(AuthError)
def authentification_failed(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        "message": ex.error['code']
                    }), 401
