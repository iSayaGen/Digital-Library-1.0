# ☙ Bibliotheca

> *A quiet collection of books, carefully catalogued.*

[![Python](https://img.shields.io/badge/Python-3.x-704b31?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-65452f?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-704b31?style=flat-square)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-database-80654b?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-Educational-8a6f52?style=flat-square)](#license)

---

## About

**Bibliotheca** is a small digital library catalogue built with **Flask, SQLAlchemy, SQLite and Jinja2**.

It allows you to:

- Add authors and books
- Search by **book title or author**
- Sort books by title or author
- Display book covers using ISBNs through Open Library
- Delete books from the collection
- Automatically remove an author when their last book is deleted
- Browse the collection through a simple antique-library inspired interface

The project is intentionally small and focused: a practical CRUD application with a little character.

---

## Preview Collection

The repository includes a sample `library.sqlite` database so that the application opens with an example collection already populated.

To start your own library, simply delete the existing books through the application and add your own authors and books.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework |
| Flask-SQLAlchemy | Database integration |
| SQLAlchemy | ORM |
| SQLite | Local database |
| Jinja2 | HTML templating |
| Open Library | Book cover images |
| HTML & CSS | Interface |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/digital-library.git
cd digital-library
```

### 2. Install dependencies

```bash
pip install -r requirements
```

### 3. Run the application

```bash
python app.py
```

The application runs on:

```text
http://localhost:5002
```

### 4. Start cataloguing

Use:

- **Add Author** to create an author
- **Add Book** to add a book to the collection
- **Search** to find books by title or author
- **Sort** to organise the catalogue

---

## Project Structure

```text
digital-library/
│
├── app.py
├── data_models.py
├── data/
│   └── library.sqlite
│
├── static/
│   └── style.css
│
└── templates/
    ├── add_author.html
    ├── add_book.html
    └── home.html
```

---

## ☙ Bibliotheca

The interface takes inspiration from old private library catalogues:

*parchment, dark wood, muted ink, and a little dust.*

The goal is not to imitate a modern book store, but to make the catalogue feel like a small personal library.

---

## License

This project was created as an educational project.

Feel free to study, modify and build upon it.