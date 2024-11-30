# E-Commerce Service

RESTful APIs using for managing an e-commerce platform, built with FastAPI and MongoDB.

---

## Features
- Manage products (add, list).
- Place orders with stock validation.
- Fully Dockerized for easy deployment.
- Unit and integration tests included.

---

## Installation

### Prerequisites
- Docker and Docker Compose installed.
- Python 3.10 (for local development and testing).

### Steps
1. Clone the repository:
    ```bash
    git clone git@github.com:Amitheshkn/e_commerce_restful_api.git
    cd e_commerce_restful_api
    ```

2. Install dependencies locally:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Create a `.env` file based on `.env.example`.
    - Example:
        ```plaintext
        MONGO_URI=mongodb://localhost:27017
        DATABASE_NAME=ecommerce
        ```

---

## Running the Application

### Locally
Start the application with Uvicorn:
```bash
uvicorn bin.e_commerce:app
