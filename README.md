# Django CSV Upload API (Dockerized)

## Overview
This API allows users to upload CSV files containing user data (**name, email, and age**) and validates the entries before saving them to the database. Invalid records are reported back in the response.

## Features
- CSV file upload with validation
- Email and age validation (0-120 years)
- Duplicate email check
- Detailed error reporting
- Swagger documentation
- Fully Dockerized setup

## Installation & Setup

### **Option 1: Run with Docker (Recommended)**
For an easy and consistent setup, use Docker:

```sh
docker-compose build  # Step 1: Build the Docker image
docker-compose up -d  # Step 2: Start the containers
docker-compose exec web python3 manage.py migrate  # Step 3: Run migrations inside the container
```

Swagger Docs: [http://localhost:8000/](http://localhost:8000/)

To stop the containers:
```sh
docker-compose down
```

### **Option 2: Manual Setup**
For local development without Docker:

```sh
python3 -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate the environment
pip install -r requirements.txt  # Install dependencies
python3 manage.py migrate  # Apply migrations
python3 manage.py runserver  # Start the server
```

## How to Upload a CSV File

### **Endpoint**
`POST /upload/`

### **Headers**
```http
Content-Type: multipart/form-data
```

### **Request (Form-Data)**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | File (.csv) | ✅ | A CSV file with `name`, `email`, and `age` |

### **CSV Example**
```csv
name,email,age
John Doe,johndoe@example.com,30
Jane Doe,janedoe@example,25
Alice,alice@example.com,200
```

## Example API Responses

### **Successful Upload**
```json
{
  "total_records_saved": 2,
  "total_records_rejected": 1,
  "error": [
    { "row": { "name": "Alice", "email": "alice@example.com", "age": "200" }, "error": "Age must be between 0 and 120." }
  ]
}
```

### **Invalid File Type**
```json
{ "error": "Invalid file type. Only CSV files are allowed." }
```

### **Invalid Email Format**
```json
{
  "total_records_saved": 1,
  "total_records_rejected": 1,
  "error": [
    { "row": { "name": "Jane Doe", "email": "janedoe@example", "age": "25" }, "error": "Invalid email format." }
  ]
}
```

### **Duplicate Email Found**
```json
{
  "total_records_saved": 0,
  "total_records_rejected": 1,
  "error": [
    { "row": { "name": "John Doe", "email": "johndoe@example.com", "age": "30" }, "error": "Email already exists." }
  ]
}
```

## Running Tests
To run tests inside the container:
```sh
docker-compose exec web python3 manage.py test
```
Or for local setup:
```sh
python3 manage.py test
```

## Developer Notes
- Swagger docs available at: **`http://localhost:8000/swagger/`**
- Rebuild the project anytime with:
  ```sh
  docker-compose up --build
  ```