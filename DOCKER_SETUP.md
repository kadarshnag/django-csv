# Docker Setup Guide for Django CSV Upload API

This guide walks you through setting up the **Django CSV Upload API** using Docker.

## 🛠️ Prerequisites
Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Steps

### **Step 1: Build the Docker Image**

```sh
docker-compose build
```

This builds the necessary containers for the project.

### **Step 2: Start the Containers**

```sh
docker-compose up -d
```

This starts the Django application and database in detached mode.

### **Step 3: Run Database Migrations**

```sh
docker-compose exec web python3 manage.py migrate
```

This applies all necessary database migrations inside the container.

### **Step 4: Access the API Documentation**

Open your browser and navigate to:

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### **Step 5: Stop the Containers**

To stop the running containers:

```sh
docker-compose down
```

## Additional Commands

### **View Logs**

```sh
docker-compose logs -f web
```

### **Rebuild and Restart Containers**

```sh
docker-compose up --build
```

### **Run Tests Inside Container**

```sh
docker-compose exec web python3 manage.py test
```

**Your Django CSV Upload API is now fully set up with Docker!**

