from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Order(db.Model):
    order_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(80), nullable=False, default='new')

    product = db.relationship('Product', backref=db.backref('orders', lazy=True))
