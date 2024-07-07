from flask_restful import Resource
from flask import request
from models import db, Order

class OrderList(Resource):
    def post(self):
        # Try to process the incoming request
        try:
            # Parse the JSON data from the request
            data = request.get_json()
            # Extract the 'orders' list from the parsed JSON data
            orders = data['orders']

            # Iterate over each order in the 'orders' list
            for order_data in orders:
                # Create a new Order object for each order in the list
                order = Order(
                    product_id=order_data['product_id'],
                    quantity=order_data['quantity']
                )
                # Add the new Order object to the database session
                db.session.add(order)

            # Commit the session to save all new Order objects to the database
            db.session.commit()

            # Placeholder for logic to notify the kitchen (not implemented)

            # Return a success message with the received orders
            return {'message': 'Orders received successfully', 'orders': orders}, 201

        # Catch a KeyError if the 'orders' key is missing in the request data
        except KeyError:
            return {'message': 'Bad request, JSON must contain "orders" key'}, 400
        # Catch any other exceptions and return an error message
        except Exception as e:
            return {'message': 'An error occurred: ' + str(e)}, 500

    def get(self):
        # Retrieve all orders from the database
        orders = Order.query.all()
        # Serialize each order into a dictionary and return as a list
        return [
            {
                "order_id": order.order_id,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "status": order.status
            } for order in orders
        ], 200