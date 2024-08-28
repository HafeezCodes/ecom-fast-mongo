# ecom-fast-mongo

Welcome to **ecom-fast-mongo**—an e-commerce application built with FastAPI and MongoDB. This project focuses on managing users, products, and a cart system.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)


## Features

- **User Management:** Handle user registration, and authentication.
- **Product Management:** Perform CRUD operations on products.
- **Cart Management:** Manage user carts, including adding and removing items.

## Technologies

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** [MongoDB](https://www.mongodb.com/)
- **Authentication:** JWT (JSON Web Tokens)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- MongoDB

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/HafeezCodes/ecom-fast-mongo.git
   cd ecom-fast-mongo
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add the necessary environment variables.

   Example `.env` file:

   ```
   MONGO_URI=your_mongodb_URI
   SECRET_KEY=your_secret_key
   JWT_ALGORITHM=HS256
   ```

### Running the Application

1. **Run the MongoDB server:**

   Make sure your MongoDB server is running online.

2. **Start the FastAPI application:**

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the application:**

   The API documentation is available at [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc).

## Project Structure

```plaintext
ecom-fast-mongo/
│
├── README.md
├── app/
│   ├── __init__.py
│   ├── constants.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── external_services/
│   ├── main.py
│   ├── routers/
│   ├── schemas/
│   ├── settings.py
│   ├── security.py
│   └── utils/
├── requirements.txt
└── tests/
    └── __init__.py
```

## API Endpoints

### Authentication

- **POST /api/users** - Register a new user
- **POST /api/users/sign_in** - Log in a user

### Products

- **GET /products/** - Get a list of products
- **POST /products/** - Create a new product
- **PUT /products/{id}** - Update a product by ID
- **DELETE /products/{id}** - Delete a product by ID

### Cart

- **GET /api/users/{user_id}/cart** - Get the user's cart
- **POST /api/users/{user_id}/cart** - Add an item to the cart by quantity 1
- **DELETE /api/users/{user_id}/cart/{cart_item_id}** - Remove an item from the cart
- **DELETE /api/users/{user_id}/cart/{product_id}/reduce** - Reduce an item count by 1
  

