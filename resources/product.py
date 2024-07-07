from flask_restful import Resource, reqparse
from flask import request
from models import db, Product

# Define the parser and request args
parser = reqparse.RequestParser()
parser.add_argument('category', type=str, required=True, help="Category cannot be blank!")
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")

class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        return [{'id': product.id, 'category': product.category, 'name': product.name} for product in products], 200

    def post(self):
        args = parser.parse_args()
        new_product = Product(
            category=args['category'],
            name=args['name']
        )
        db.session.add(new_product)
        db.session.commit()
        return {'message': 'Product added successfully', 'product': {'id': new_product.id, 'category': new_product.category, 'name': new_product.name}}, 201

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {'id': product.id, 'category': product.category, 'name': product.name}, 200

    def put(self, product_id):
        args = parser.parse_args()
        product = Product.query.get_or_404(product_id)
        product.category = args['category']
        product.name = args['name']
        db.session.commit()
        return {'message': 'Product updated successfully', 'product': {'id': product.id, 'category': product.category, 'name': product.name}}, 200

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 204
