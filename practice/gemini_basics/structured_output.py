import os
from pathlib import Path
from enum import Enum
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai
from google.genai import types

# Load API key
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"


# ============================================================
# SIMPLE / FLAT STRUCTURE
# ============================================================

class Book(BaseModel):
    title: str
    author: str
    genre: str
    rating: float


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=Book,
)

response = client.models.generate_content(
    model=model,
    contents="Give me information about the book Dune by Frank Herbert.",
    config=config,
)

book = Book.model_validate_json(response.text)

print("=== 1. SIMPLE OBJECT ===")
print(book)


# ============================================================
# NESTED OBJECT
# ============================================================

class Author(BaseModel):
    name: str
    nationality: str


class BookWithAuthor(BaseModel):
    title: str
    genre: str
    rating: float
    author: Author


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=BookWithAuthor,
)

response = client.models.generate_content(
    model=model,
    contents="Give me information about Dune by Frank Herbert, including author details.",
    config=config,
)

book = BookWithAuthor.model_validate_json(response.text)

print("\n=== 2. NESTED OBJECT ===")
print(book)
print(f"Author name: {book.author.name}")
print(f"Nationality: {book.author.nationality}")


# ============================================================
# LIST OF OBJECTS
# ============================================================

class BookSummary(BaseModel):
    title: str
    author: str
    genre: str


class BookList(BaseModel):
    books: list[BookSummary]


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=BookList,
)

response = client.models.generate_content(
    model=model,
    contents="Give me 3 famous science fiction books.",
    config=config,
)

books = BookList.model_validate_json(response.text)

print("\n=== 3. LIST OF OBJECTS ===")

for book in books.books:
    print(f"- {book.title} by {book.author} ({book.genre})")


# ============================================================
# OBJECT WITH LISTS
# ============================================================

class Movie(BaseModel):
    title: str
    director: str
    genres: list[str]
    actors: list[str]


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=Movie,
)

response = client.models.generate_content(
    model=model,
    contents="Give me information about the movie Inception.",
    config=config,
)

movie = Movie.model_validate_json(response.text)

print("\n=== 4. OBJECT WITH LISTS ===")
print(f"Title: {movie.title}")
print(f"Director: {movie.director}")
print(f"Genres: {movie.genres}")
print(f"Actors: {movie.actors}")


# ============================================================
# ENUM / FIXED CHOICES
# ============================================================

class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProgrammingTopic(BaseModel):
    topic: str
    difficulty: Difficulty
    description: str


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=ProgrammingTopic,
)

response = client.models.generate_content(
    model=model,
    contents="Explain Python decorators for a programming student.",
    config=config,
)

topic = ProgrammingTopic.model_validate_json(response.text)

print("\n=== 5. ENUM / FIXED CHOICES ===")
print(f"Topic: {topic.topic}")
print(f"Difficulty: {topic.difficulty}")
print(f"Description: {topic.description}")


# ============================================================
# OPTIONAL FIELDS
# ============================================================

class Person(BaseModel):
    name: str
    age: int
    occupation: Optional[str] = None
    email: Optional[str] = None


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=Person,
)

response = client.models.generate_content(
    model=model,
    contents="Give me basic information about Albert Einstein.",
    config=config,
)

person = Person.model_validate_json(response.text)

print("\n=== 6. OPTIONAL FIELDS ===")
print(person)


# ============================================================
# COMPLEX NESTED STRUCTURE
# ============================================================

class Review(BaseModel):
    reviewer: str
    rating: float
    comment: str


class Product(BaseModel):
    name: str
    category: str
    price: float
    features: list[str]
    reviews: list[Review]


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=Product,
)

response = client.models.generate_content(
    model=model,
    contents="Create product information for a wireless mechanical keyboard with 2 reviews.",
    config=config,
)

product = Product.model_validate_json(response.text)

print("\n=== 7. COMPLEX NESTED STRUCTURE ===")
print(f"Product: {product.name}")
print(f"Category: {product.category}")
print(f"Price: {product.price}")
print(f"Features: {product.features}")

print("\nReviews:")

for review in product.reviews:
    print(f"- {review.reviewer}: {review.rating}/5")
    print(f"  {review.comment}")
