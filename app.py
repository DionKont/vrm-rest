from flask import Flask
from flask_restful import Api
from models import db, Product, Order
from resources.hello import HelloWorld
from resources.product import ProductList, ProductResource
from resources.order import OrderList

def create_app():
    try:
        # Initialize Flask app
        app = Flask(__name__)

        # Database configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialize SQLAlchemy with Flask app
        db.init_app(app)

        # Initialize Flask-RESTful Api with Flask app
        api = Api(app)

        # Register resource routes
        api.add_resource(HelloWorld, '/')
        api.add_resource(ProductList, '/products')
        api.add_resource(ProductResource, '/products/<int:product_id>')
        api.add_resource(OrderList, '/orders')

        # Create database tables
        with app.app_context():
            db.create_all()

        return app
    except Exception as e:
        print(f"An error occurred during app initialization: {e}")
        return None

if __name__ == '__main__':
    app = create_app()
    if app:
        try:
            app.run(debug=True)
        except Exception as e:
            print(f"An error occurred while running the app: {e}")
    else:
        print("Failed to initialize the Flask application.")
