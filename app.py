from pathlib import Path
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from data_models import Author, Book, db


app = Flask(__name__)


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "library.sqlite"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
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
    """Display the author form and add a unique author."""

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            return render_template(
                "add_author.html",
                error="Author name cannot be empty."
            )

        if len(name) > 100:
            return render_template(
                "add_author.html",
                error="Author name must be 100 characters or fewer."
            )

        existing_author = Author.query.filter(
            db.func.lower(Author.name) == name.lower()
        ).first()

        if existing_author:
            return render_template(
                "add_author.html",
                error="An author with this name already exists."
            )

        birth_date_input = request.form.get(
            "birth_date", ""
        ).strip()

        birth_date = None

        if birth_date_input:
            birth_date = datetime.strptime(
                birth_date_input,
                "%Y-%m-%d"
            ).date()

        date_of_death_input = request.form.get(
            "date_of_death", ""
        ).strip()

        date_of_death = None

        if date_of_death_input:
            date_of_death = datetime.strptime(
                date_of_death_input,
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
    """Display the book form and add a book with a unique ISBN."""

    authors = Author.query.order_by(Author.name).all()

    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()

        if not isbn:
            return render_template(
                "add_book.html",
                authors=authors,
                error="ISBN cannot be empty."
            )

        if len(isbn) > 20:
            return render_template(
                "add_book.html",
                authors=authors,
                error="ISBN must be 20 characters or fewer."
            )

        if not title:
            return render_template(
                "add_book.html",
                authors=authors,
                error="Book title cannot be empty."
            )

        existing_book = Book.query.filter_by(isbn=isbn).first()

        if existing_book:
            return render_template(
                "add_book.html",
                authors=authors,
                error="A book with this ISBN already exists."
            )

        publication_year = int(request.form["publication_year"])
        author_id = int(request.form["author_id"])

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
