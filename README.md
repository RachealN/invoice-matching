
# Invoices Matching Tool

This project is a RESTful API built using Flask and React, designed to match invoice line items with a list of deliveries based on delivery numbers. The application provides a set of endpoints for data reconciliation and includes Docker configuration for seamless setup and deployment.

## Setup Instructions

### Prerequisites

Make sure you have the following installed on your machine:

- **Python 3.8 and above**  
  [Installation Guide](https://www.python.org/downloads/)
- **Docker**  
  [Installation Guide](https://docs.docker.com/get-docker/)
- **MySQL**  
  *(The MySQL service is run inside Docker, so you don't need a local installation unless you plan to use it outside Docker.)*
- **Git**  
  [Installation Instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

---

### 1. Clone the Repository

Clone your project repository to your local machine using Git.

```bash
git clone git@github.com:RachealN/invoice-matching.git
cd invoice-matching
```

---

### 2. Build and Run the Containers

In the root project directory, run the following command to build the Docker images and start the containers:

```bash
docker-compose up --build
```

This command will build the images for the API, Client, and Database services and start them. You can interact with your Docker containers using these commands:

- **Access a Container**:  
  ```bash
  docker-compose exec -it <container_name> bash
  ```
  Replace `<container_name>` with `api`, `react-client`, or `mysql-db` as appropriate.

- **Check Container Status**:  
  ```bash
  docker-compose ps
  ```

- **View Logs in Real Time**:  
  ```bash
  docker-compose up
  ```

- **Run Containers in the Background (Detached Mode)**:  
  ```bash
  docker-compose up -d
  ```

- **Stop and Remove Containers**:  
  ```bash
  docker-compose down
  ```

- **Watch Container Logs**:  
  ```bash
  docker-compose logs
  ```

---

### 3. Running Database Migrations and Seeding Data

Before using the application, ensure that your database schema is up-to-date and seeded with initial data. This project uses Flask-Migrate for database migrations.

#### **Running Migrations**
1. **Access the API Container**:  
   Open a terminal session into the `api` container:

   ```bash
   docker-compose exec api bash
   ```

2. **Run Migrations**:  
   Within the container, execute the migration command to apply any pending migrations:

   ```bash
   flask db upgrade
   ```

   If you're setting up the database for the first time, you might need to initialize the migration repository first:

   ```bash
   flask db init
   flask db migrate -m "Initial migration." -  Feel free to use message of your choice
   flask db upgrade
   ```

#### **Seeding the Database**
After running the migrations, you can seed the database with initial data.

1. Inside the `api` container, run:

   ```bash
   python3 app/seeders/seed.py
   ```
This command should execute a predefined seeding script that inserts sample data into  database.
The database should be properly structured and populated with sample data for testing.

### 4.Endpoints

Once the containers are running and the migrations have been applied, you can test the following endpoints:

- **List All Invoices**:  
  **GET** `/invoices/all`

- **List All Deliveries**:  
  **GET** `/deliveries/all`

- **Match Invoices with Deliveries**:  
  **POST** `/invoices/match`

  **Payload Example:**

  ```json
  {
    "invoice_items": [
      {
        "delivery_number": "DEL-00011",
        "title": "Item Z",
        "unit": "pcs",
        "amount": 50.0,
        "price": 5000.0
      }
    ],
    "delivery_numbers": {
      "DEL-00011": {
        "supplier_name": "Supplier X",
        "line_items": [
          {
            "title": "Item Z",
            "unit": "pcs",
            "amount": 50.0
          }
        ]
      }
    }
  }
  ```

### 5. Running Unit Tests

To run the unit tests for the API endpoints, you can use `pytest`. This can be done either inside the Docker container or directly on your local machine if you have Python and pytest installed.

**Inside the Docker Container:**

1. Access the `api` container:

   ```bash
   docker-compose exec api bash
   ```

2. Run the tests:

   ```bash
   pytest app/tests/tests.py
   ```

## Additional Notes

- **Volume Mounting for Development**:  
  The `api` service mounts the project directory into the container (`.:/app`). This allows changes to the code to be immediately reflected during development.

- **Service Dependencies**:  
  The API service depends on the MySQL service (`db`), ensuring that the database is started first. Similarly, the React client depends on the API service.

- **Environment Configuration**:  
  Environment variables are defined directly in the `docker-compose.yml` file for simplicity. If your project grows or requires additional configurations, consider using a dedicated `.env` file.

 You should now be able to set up, run, and evaluate your Invoices Matching Tool locally.