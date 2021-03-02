# Ecommere API

## Motivation 
This is an ecommerce API which lists products in an ecommerce website and their categories, where you can view, add, edit or delete any of them, based on your role. The roles using this API are the user and admin. The website has no front-end so far, but it will be implemented in the near future. It is done as a graduation project for the Udacity Full Stack Nanodegree.

All code follows PEP8 style guide.

## Getting Started

### How to access the API app?

The API is deployed at https://ecommerce-api-udacity.herokuapp.com/. 

### Authorization 

You can access the API through several methods:

- Using the user and admin tokens included in the setup.sh file
- I attached a postman collection with all the endpoins included; the tokens (user and admin) are saved as global variables in the environment
- If the tokens expired, please navigate to 
https://ecommerce-api-udacity.herokuapp.com/authorization/url and enter the credentials. You will be directed to a link where you can extract the token from the address bar. The credentials for the roles will be in the roles secion of the documentation and will be added to the submission notes.

### Installing Dependencies Locally

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create a new database:

```
createdb ecommerce
``` 
Then go to `backend/src` and run:

```
python manage.py db upgrade
``` 


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, go to `backend/src`:

Set up environment variables using:

```
source setup.sh
```
Then execute:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```

## API Reference 

### Getting Started

- Base URL: This app can be run locally at the default, http://127.0.0.1:5000/, and it is hosted on a base URL, https://ecommerce-api-udacity.herokuapp.com/.
- Authentication: This version of the application requires authentication for all APIs. It uses Auth0 for authentication and login.

## Roles

The API has two roles
- User: can view all products, product by ID, products by category, all categories, and cateogry by ID.
email: marwa.mrashad@gmail.com
password: Ecommerce123*

- Admin: has full access to all endpoints.
email: admin@ecommerce.com
password: Ecommerce123*

### Error Handling
Errors are returned as JSON objects in the following format:
```
{      "success": False, 
        "error": 404,
        "message": "Not found"
        }
```

The API will return the following types when requests fail:
-	400: Bad Request
-	404: Not Found
-	422: Unprocessable Entity
-   405: Method Not Allowed
-   500: Internal Server Error
-   401: Unauthorized 
### Endpoints

To avoid redundacny in the API documentation, this is a refernece of the main object types.

##### product
An object of name: name_string, category_id: category_id_number, description: product_description, id: product_id, and price: price_string key:value pairs.

##### category

An object of id: category_id, type: category_type, description: category_description,  key:value pairs.


#### GET '/products'

- Fetches a dictionary of products, success value.
- Request arguments: admin/user token in the header
- Roles with access: admin, user
- Returns: An object with a success:value key:value pair, products: list of product objects key:value pair.
- Sample: `curl http://127.0.0.1:5000/products`
```{
    "products": [
        {
            "category_id": 1,
            "description": " baby skirt",
            "id": 1,
            "name": "Skirt",
            "price": "500"
        },
        {
            "category_id": 1,
            "description": " baby shorts",
            "id": 2,
            "name": "Shorts",
            "price": "500"
        },
        {
            "category_id": 2,
            "description": "women blouse",
            "id": 3,
            "name": "Blouse",
            "price": "500"
        },
        {
            "category_id": 2,
            "description": "women dress",
            "id": 4,
            "name": "Dress",
            "price": "500"
        },
        {
            "category_id": 3,
            "description": "men pants",
            "id": 5,
            "name": "Pants",
            "price": "500"
        },
        {
            "category_id": 3,
            "description": "men shorts",
            "id": 6,
            "name": "Shorts",
            "price": "500"
        }
    ],
    "success": true
}

```
#### POST '/products'
- Creates a new product using the submitted name, description, price, category_id.
- Request arguments: product object, admin token in the header
- Roles with access: admin, user
- Returns: an object with a success:value key:value pair and added product data.

#### PATCH '/products/<int:product_id>'
- Edits an existing product using the submitted name, description, price, or category_id.
- Request argument: product ID, product object field to be edited and its value, admin token in the header.
- Roles with access: admin
- Returns: an object with a success:value key:value pair and edited product data.

#### DELETE '/products/<int:product_id>'

- If provided, deletes the specified product.
- Request argument: product ID, admin token in the header.
- Roles with access: admin
- Returns: an object of success: value key:value pairs and delete: deleted_question_id key:value pairs.

#### GET '/questions/category/<int:category_id>'

- Fetches a dictionary of products based on the submitted category ID.
- Request argument: category ID, admin/user token in the header.
- Roles with access: admin, user
- Returns: An object with a success:value key:value pair, products: list of product objects key:value pair







#### GET '/categories'

- Fetches a dictionary of categories, success value.
- Request arguments: admin/user token in the header
- Roles with access: admin, user
- Returns: An object with a success:value key:value pair, categories: list of category objects key:value pair.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
    "categories": [
        {
            "description": "for kids",
            "id": 1,
            "type": "kids"
        },
        {
            "description": "for women",
            "id": 2,
            "type": "women"
        },
        {
            "description": "for men",
            "id": 3,
            "type": "men"
        },
        {
            "description": "delete me",
            "id": 4,
            "type": "delete"
        }
    ],
    "success": true
}
```
#### POST '/categories'
- Creates a new category using the submitted type, description, id.
- Request arguments: category object, admin token in the header
- Roles with access: admin, user
- Returns: an object with a success:value key:value pair and added category data.

#### PATCH '/categories/<int:category_id>'
- Edits an existing category using the submitted type or description.
- Request argument: category ID, category object field to be edited and its value, admin token in the header.
- Roles with access: admin
- Returns: an object with a success:value key:value pair and edited category data.

#### DELETE '/categories/<int:category_id>'

- If provided, deletes the specified category.
- Request argument: category ID, admin token in the header.
- Roles with access: admin
- Returns: an object of success: value key:value pairs and delete: deleted_category_id key:value pairs.

## Testing
To run the tests, run
```
python test_app.py
```
Tokens are added in test_app.py for testing purposes.