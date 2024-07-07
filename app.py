from flask import Flask
from flask_restful import Api
from models import db, Product, Order
from resources.hello import HelloWorld
from resources.product import ProductList, ProductResource
from resources.order import OrderList

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    api = Api(app)

    api.add_resource(HelloWorld, '/')
    api.add_resource(ProductList, '/products')
    api.add_resource(ProductResource, '/products/<int:product_id>')
    api.add_resource(OrderList, '/orders')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
