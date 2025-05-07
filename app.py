from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Use PostgreSQL/MySQL in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
auth = HTTPBasicAuth()

# In-memory user store for demonstration
users = {
    "admin": generate_password_hash("password123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published_year": self.published_year,
            "isbn": self.isbn
        }

def validate_book_data(data):
    if not all(k in data for k in ("title", "author", "published_year", "isbn")):
        abort(400, description="Missing required book fields.")
    if not isinstance(data["published_year"], int):
        abort(400, description="published_year must be an integer.")

class BookListResource(Resource):
    @auth.login_required
    def get(self):
        books = Book.query.all()
        return [book.to_dict() for book in books], 200

    @auth.login_required
    def post(self):
        data = request.get_json()
        validate_book_data(data)
        if Book.query.filter_by(isbn=data["isbn"]).first():
            abort(400, description="Book with this ISBN already exists.")
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return book.to_dict(), 201

class BookResource(Resource):
    @auth.login_required
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book.to_dict(), 200

    @auth.login_required
    def put(self, book_id):
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        validate_book_data(data)
        if data["isbn"] != book.isbn and Book.query.filter_by(isbn=data["isbn"]).first():
            abort(400, description="Book with this ISBN already exists.")
        book.title = data["title"]
        book.author = data["author"]
        book.published_year = data["published_year"]
        book.isbn = data["isbn"]
        db.session.commit()
        return book.to_dict(), 200

    @auth.login_required
    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204

api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)