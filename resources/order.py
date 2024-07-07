from flask_restful import Resource
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import db, Order

class OrderList(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'orders' not in data:
                return {'message': 'Bad request, JSON must contain "orders" key'}, 400

            orders = data['orders']

            for order_data in orders:
                order = Order(
                    product_id=order_data['product_id'],
                    quantity=order_data['quantity']
                )
                db.session.add(order)

            db.session.commit()

            # Placeholder for logic to notify the kitchen (not implemented)

            return {'message': 'Orders received successfully', 'orders': orders}, 201

        except KeyError as e:
            return {'message': f'Key error: {str(e)}'}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Database error: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500

    def get(self):
        try:
            orders = Order.query.all()
            if not orders:
                return {'message': 'No orders found'}, 404
            
            result = [
                {
                    "order_id": order.order_id,
                    "product_id": order.product_id,
                    "quantity": order.quantity,
                    "status": order.status
                } for order in orders
            ]
            return result, 200
        
        except SQLAlchemyError as e:
            return {'message': f'Database error: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500
