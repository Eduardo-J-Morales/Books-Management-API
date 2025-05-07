from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Falsk(__name__)
api = Api(app)

db = SQLAlchemy(app)

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("password123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    published_date = db.Column(db.String(10), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date,
        }
    
def validate_book_data(data):
    if not all(key in data for key in ('title', 'author', 'published_date', 'isbn')):
        abort(400, 'Missing required fields')
    if not isinstance(data['published_date'], int):
        abort(400, 'Published date must be an integer')
    
class BookResource(Resource):
    @auth.login_required
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict())
    
    @auth.login_required
    def post(self):
        data = request.get_json()
        validate_book_data(data)
        if Book.query.filter_by(isbn=data['isbn']).first():
            abort(400, 'Book with this ISBN already exists')
