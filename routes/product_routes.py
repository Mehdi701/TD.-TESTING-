from flask import Blueprint, request, jsonify
from models.database import db
from models.product import Product

product_routes = Blueprint("product_routes", __name__)

@product_routes.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@product_routes.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"error": "Product not found"}), 404

@product_routes.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data.get("name") or data.get("price") is None:
        return jsonify({"error": "Name and price are required"}), 400

    new_product = Product(name=data["name"], price=data["price"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@product_routes.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    db.session.commit()
    return jsonify(product.to_dict()), 200

@product_routes.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
