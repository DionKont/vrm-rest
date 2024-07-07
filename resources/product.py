from flask_restful import Resource, reqparse
from flask import request
from models import db, Product

# Initialize the request parser
parser = reqparse.RequestParser()
# Define required arguments for the parser
parser.add_argument('category', type=str, required=True, help="Category cannot be blank!")
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")

class ProductList(Resource):
    def get(self):
        # Retrieve all products from the database
        products = Product.query.all()
        # Serialize the product data to send as JSON
        return [{'id': product.id, 'category': product.category, 'name': product.name} for product in products], 200

    def post(self):
        # Parse the request arguments
        args = parser.parse_args()
        # Create a new product instance with the provided arguments
        new_product = Product(
            category=args['category'],
            name=args['name']
        )
        # Add the new product to the database session and commit to save
        db.session.add(new_product)
        db.session.commit()
        # Return a success message with the added product's information
        return {'message': 'Product added successfully', 'product': {'id': new_product.id, 'category': new_product.category, 'name': new_product.name}}, 201

class ProductResource(Resource):
    def get(self, product_id):
        # Retrieve a product by its ID or return 404 if not found
        product = Product.query.get_or_404(product_id)
        # Return the product's data
        return {'id': product.id, 'category': product.category, 'name': product.name}, 200

    def put(self, product_id):
        # Parse the request arguments
        args = parser.parse_args()
        # Retrieve the product to update or return 404 if not found
        product = Product.query.get_or_404(product_id)
        # Update the product's category and name with the provided arguments
        product.category = args['category']
        product.name = args['name']
        # Commit the changes to the database
        db.session.commit()
        # Return a success message with the updated product's information
        return {'message': 'Product updated successfully', 'product': {'id': product.id, 'category': product.category, 'name': product.name}}, 200

    def delete(self, product_id):
        # Retrieve the product to delete or return 404 if not found
        product = Product.query.get_or_404(product_id)
        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()
        # Return a success message indicating deletion
        return {'message': 'Product deleted successfully'}, 204