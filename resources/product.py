from flask_restful import Resource, reqparse
from flask import request
from models import db, Product
from datetime import datetime

# Define the parser and request args
parser = reqparse.RequestParser()
parser.add_argument('category', type=str, required=True, help="Category cannot be blank!")
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
parser.add_argument('stock_quantity', type=int, required=True, help="Stock quantity cannot be blank!")
parser.add_argument('status', type=str, default='available')
parser.add_argument('allergy_information', type=str)


def serialize_product(product):
    return {
        'id': product.id,
        'category': product.category,
        'name': product.name,
        'price': product.price,
        'stock_quantity': product.stock_quantity,
        'status': product.status,
        'allergy_information': product.allergy_information,
        'created_at': product.created_at.isoformat()  # Convert datetime to ISO format string
    }


class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        return [serialize_product(product) for product in products], 200

    def post(self):
        args = parser.parse_args()

        # Check for duplicate product
        existing_product = Product.query.filter_by(category=args['category'], name=args['name']).first()
        if existing_product:
            return {'message': 'Product already exists'}, 400

        new_product = Product(
            category=args['category'],
            name=args['name'],
            price=args['price'],
            stock_quantity=args['stock_quantity'],
            status=args['status'],
            allergy_information=args.get('allergy_information')
        )
        db.session.add(new_product)
        db.session.commit()
        return {'message': 'Product added successfully', 'product': serialize_product(new_product)}, 201


class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return serialize_product(product), 200

    def put(self, product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.category = data.get('category', product.category)
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.status = data.get('status', product.status)
        product.allergy_information = data.get('allergy_information', product.allergy_information)
        db.session.commit()
        return {'message': 'Product updated successfully', 'product': serialize_product(product)}, 200

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 204
