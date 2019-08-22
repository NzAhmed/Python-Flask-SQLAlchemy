# Create a web API with python + Flask + PostgreSQL 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app with SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgresql@localhost/shopping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    categoryId = db.Column(db.Integer, nullable=True)
    isActive = db.Column(db.Boolean, default=False, nullable=False)
    dateCreated = db.Column(db.Date)

    # serialize is useful when we need to return product objects in response as JSON
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'categoryId': self.categoryId,
            'isActive':self.isActive,
	    'dateCreaed': self.dateCreated
        }

##### POST API #######################################################
@app.route("/api/products", methods=["POST"])
def add_product():
    name = request.json['name']
    categoryId = request.json['categoryId']
    isActive = request.json['isActive']
    dateCreated = request.json['dateCreated']

    product = Product(
        name = name, 
        categoryId = categoryId, 
        isActive = isActive, 
        dateCreated = dateCreated
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.serialize())

##### GET by id API ###################################################
@app.route("/api/products/<id>", methods=["GET"])
def product_detail(id):
    product = Product.query.get(id)
    if not product:
        return 'Not Found'
    #return jsonify(id=product.id,name=product.name)
    return jsonify(product.serialize())

##### GET all API #####################################################
@app.route("/api/products", methods=["GET"])
def product_get():
    all_products = Product.query.all()
    products = Product.query.all()
    return  jsonify([product.serialize() for product in products])

##### PUT API #########################################################
@app.route("/api/products/<id>", methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)
    name = request.json['name']
    categoryId = request.json['categoryId']
    isActive = request.json['isActive']
    dateCreated = request.json['dateCreated']

    product.name = name
    product.categoryId = categoryId
    product.isActive = isActive
    product.dateCreated = dateCreated

    db.session.commit()
    return '', 204

##### DELETE API ######################################################
@app.route("/api/products/<id>", methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    if not product:
        return 'Not Found'

    db.session.delete(product)
    db.session.commit()
    return 'No Content'


if __name__ == '__main__':
    app.run(debug=True)


"""
https://www.tutorialspoint.com/flask/flask_sqlalchemy.htm
"""
