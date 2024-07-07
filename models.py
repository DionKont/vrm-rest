from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(80), nullable=False, default='available')
    allergy_information = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
        self.validate_price()
        self.validate_stock_quantity()

    def validate_price(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")

    def validate_stock_quantity(self):
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")

class Order(db.Model):
    order_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(80), nullable=False, default='new')
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.validate_quantity()

    def validate_quantity(self):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1")