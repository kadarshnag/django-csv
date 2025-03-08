# Step 1: Build the Docker image
docker-compose build

# Step 2: Start the containers
docker-compose up -d

# Step 3: Run migrations inside the container
docker-compose exec web python3 manage.py migrate

# Step 4: Open the swagger to check API
http://localhost:8000/
