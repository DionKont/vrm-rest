from flask_restful import Resource
from flask import request
from models import db, Order

class OrderList(Resource):
    def post(self):
        try:
            data = request.get_json()
            orders = data['orders']

            for order_data in orders:
                order = Order(
                    product_id=order_data['product_id'],
                    quantity=order_data['quantity']
                )
                db.session.add(order)

            db.session.commit()
            
            # Here, you would add logic to notify the kitchen, e.g., through a message queue or another mechanism.

            return {'message': 'Orders received successfully', 'orders': orders}, 201

        except KeyError:
            return {'message': 'Bad request, JSON must contain "orders" key'}, 400
        except Exception as e:
            return {'message': 'An error occurred: ' + str(e)}, 500
    
    
    def get(self):
        orders = Order.query.all()
        return [
            {
                "order_id": order.order_id,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "status": order.status
            } for order in orders
        ], 200



#Babis