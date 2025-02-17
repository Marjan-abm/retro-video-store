from flask import Blueprint, jsonify, make_response, request

from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from app.rental_routes import deletes_rentals

customers_bp = Blueprint("customers",__name__, url_prefix="/customers")

@customers_bp.route("",methods=["GET"])

def get_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())

    return jsonify(customers_response),200

@customers_bp.route("/<customer_id>",methods=["GET"])
def get_customer_by_id(customer_id):
    
    try:
        customer_id = int(customer_id)
    except ValueError:
        return make_response(jsonify({"error": "Invalid ID"}), 400)
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response(jsonify({'message': f'Customer {customer_id} was not found'}),404)
    return customer.to_dict(),200

@customers_bp.route("/<cust_id>/rentals",methods=["GET"])
def get_customer_rentals(cust_id):

    customer = Customer.query.get(cust_id)
    if not customer:
        return make_response(jsonify({'message': f'Customer {cust_id} was not found'}),404)

    all_rentals = []
    rentals = db.session.query(Rental).filter(Rental.customer_id==cust_id).all()
    for rental in rentals:
        video = Video.query.get(rental.video_id)
        all_rentals.append({"title":video.title})
    return make_response(jsonify(all_rentals),200)

@customers_bp.route("",methods=["POST"])
def new_customer():
    request_body = request.get_json()
    try:
        customer = Customer(name=request_body["name"],
        postal_code = request_body["postal_code"],
        phone=request_body["phone"])

    except KeyError:
        if "name" not in request_body:
            return make_response({"details":"Request body must include name."}, 400)
        elif "phone" not in request_body:
            return make_response({"details":"Request body must include phone."}, 400)
        elif "postal_code" not in request_body:
            return make_response({"details":"Request body must include postal_code."}, 400)

    db.session.add(customer)
    db.session.commit()

    return make_response({
        "id":customer.customer_id
    }, 201)

@customers_bp.route("/<customer_id>",methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    try:
        customer_id = int(customer_id)
    except ValueError:
        return 400
    if not customer:
        return make_response(jsonify({'message': f'Customer {customer_id} was not found'}),404)
    deletes_rentals(customer.customer_id, True)
    db.session.delete(customer)
    db.session.commit()

    return make_response({
        "id":customer.customer_id
    }, 200)

@customers_bp.route("/<customer_id>",methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response(jsonify({'message': f'Customer {customer_id} was not found'}),404)
    form_data = request.get_json()

    try:
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

    except KeyError:
        return make_response({
            "details":"Invalid data"
        }, 400)
    db.session.commit()
    return customer.to_dict(),200
