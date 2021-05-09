import pytest
from app import db
from app.models.book import Book

def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book", description="watr 4evr")
    mountain_book = Book(title="Mountain Book", description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()

def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_one_book_not_in_db(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

def test_get_all_books_with_records(client,two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr",
    },
    {
        "id": 2,
        "title": "Mountain Book",
        "description":"i luv 2 climb rocks"
    }]

@pytest.fixture
def book_data(app):
    return {
        "title": "Fire Book",
        "description": "hot hot hot"
        }

def test_create_one_book(client, book_data):
    response = client.post("/books", json=book_data)
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Book Fire Book successfully created"
