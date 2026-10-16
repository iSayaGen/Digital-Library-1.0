from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Represent an author in the library."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship("Book", back_populates="author", lazy=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return self.name


class Book(db.Model):
    """Represent a book in the library."""

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return self.title
