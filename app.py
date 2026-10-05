import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from data_models import Author, Book, db


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    """Display the library catalogue with search and sorting."""

    search = request.args.get("search", "").strip()
    sort = request.args.get("sort")
    deleted = request.args.get("deleted")

    if search:
        books = (
            Book.query
            .join(Author)
            .filter(
                db.or_(
                    Book.title.ilike(f"%{search}%"),
                    Author.name.ilike(f"%{search}%")
                )
            )
            .all()
        )
    else:
        books = Book.query.all()

    if sort == "title":
        books = sorted(
            books,
            key=lambda book: book.title.lower()
        )

    elif sort == "author":
        books = sorted(
            books,
            key=lambda book: book.author.name.lower()
        )

    return render_template(
        "home.html",
        books=books,
        search=search,
        deleted=deleted
    )


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Display the author form and add a new author."""

    if request.method == "POST":
        name = request.form["name"]

        birth_date = datetime.strptime(
            request.form["birth_date"],
            "%Y-%m-%d"
        ).date()

        date_of_death = None

        if request.form["date_of_death"]:
            date_of_death = datetime.strptime(
                request.form["date_of_death"],
                "%Y-%m-%d"
            ).date()

        author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(author)
        db.session.commit()

        return render_template(
            "add_author.html",
            success="Author successfully added!"
        )

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Display the book form and add a new book."""

    authors = Author.query.all()

    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]

        publication_year = int(
            request.form["publication_year"]
        )

        author_id = int(
            request.form["author_id"]
        )

        book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(book)
        db.session.commit()

        return render_template(
            "add_book.html",
            authors=authors,
            success="Book successfully added!"
        )

    return render_template(
        "add_book.html",
        authors=authors
    )


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Delete a book and remove its author if no books remain."""

    book = Book.query.get_or_404(book_id)

    book_title = book.title
    author = book.author

    db.session.delete(book)
    db.session.commit()

    remaining_books = Book.query.filter_by(
        author_id=author.id
    ).count()

    if remaining_books == 0:
        db.session.delete(author)
        db.session.commit()

    return redirect(
        url_for(
            "home",
            deleted=book_title
        )
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5002
    )
