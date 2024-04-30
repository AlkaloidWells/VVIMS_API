

---

# VVIMS

Short project description here.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Database Structure](#database-structure)
- [Frontend Usage](#frontend-usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Provide a brief introduction to the project, its purpose, and its goals.

## Features

List the key features of the project.

- Feature 1: Description
- Feature 2: Description
- ...

## Technologies Used

List the technologies/frameworks/libraries used in the project.

- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- ...

## Installation

Provide instructions for setting up the project locally.

1. Clone the repository: `git clone https://github.com/username/repository.git`
2. Navigate to the project directory: `cd TEST_API`
3. Install dependencies: `pip3 install -r requirements.txt`
4. Run migrations: `flask db upgrade`
5. Start the server: `flask run`

## API Documentation

### User API
**base url /api/v1/auth

Authentication
Register User
Endpoint: /register
Method: POST
Description: Register a new user with the system.
Request Body:

username (string, required): The username of the user.
email (string, required): The email address of the user.
password (string, required): The password of the user.
User Login
Endpoint: /login
Method: POST
Description: Authenticate a user and generate access and refresh tokens.
Request Body:

username (string, required): The username of the user.
password (string, required): The password of the user.
Get Current User
Endpoint: /me
Method: GET
Description: Retrieve details of the currently authenticated user.
Authorization: JWT token required in the request headers.

Refresh Access Token
Endpoint: /token/refresh
Method: GET
Description: Refresh the access token using the refresh token.
Authorization: JWT token required in the request headers.

User Management
Get All Users
Endpoint: /all_users
Method: GET
Description: Retrieve details of all users in the system.
Authorization: JWT token required in the request headers.

Get User by ID
Endpoint: /user/{id}
Method: GET
Description: Retrieve details of a specific user by their ID.
Authorization: JWT token required in the request headers.

Delete User
Endpoint: /{id}
Method: DELETE
Description: Delete a user from the system by their ID.
Authorization: JWT token required in the request headers.

Role-based Authorization
Get Role
Endpoint: /role
Method: GET
Description: Retrieve the role of the current user.
Authorization: JWT token required in the request headers.
Permissions: Only accessible to users with roles other than 'staff'.

.

### Staff User API

#### Create Staff User

- **Endpoint:** `/api/staff_users`
  - **Method:** POST
  - **Description:** Creates a new staff user.
  - **Parameters:** JSON data containing username, password, role, image_path, full_name, date_emp, address, and contact_details.
  - **Response:** Message indicating successful staff user creation or error message.

#### Delete Staff User

- **Endpoint:** `/api/staff_users/<int:user_id>`
  - **Method:** DELETE
  - **Description:** Deletes a staff user with the specified user ID.
  - **Response:** Message indicating successful staff user deletion or error message.

#### Update Staff User

- **Endpoint:** `/api/staff_users/<int:user_id>`
  - **Method:** PUT
  - **Description:** Updates staff user information.
  - **Parameters:** JSON data containing fields to be updated.
  - **Response:** Message indicating successful staff user update or error message.

### Visitor API

#### Create Visitor

- **Endpoint:** `/api/visitors`
  - **Method:** POST
  - **Description:** Registers a new visitor.
  - **Parameters:** JSON data containing visitor information.
  - **Response:** Message indicating successful visitor registration or error message.

#### Update Visitor

- **Endpoint:** `/api/visitors/<int:visitor_id>`
  - **Method:** PUT
  - **Description:** Updates visitor information.
  - **Parameters:** JSON data containing fields to be updated.
  - **Response:** Message indicating successful visitor update or error message.

#### Delete Visitor

- **Endpoint:** `/api/visitors/<int:visitor_id>`
  - **Method:** DELETE
  - **Description:** Deletes a visitor with the specified visitor ID.
  - **Response:** Message indicating successful visitor deletion or error message.

### Vehicle API

#### Register Vehicle

- **Endpoint:** `/api/vehicles`
  - **Method:** POST
  - **Description:** Registers a new vehicle.
  - **Parameters:** JSON data containing vehicle information.
  - **Response:** Message indicating successful vehicle registration or error message.

#### Update Vehicle

- **Endpoint:** `/api/vehicles/<int:vehicle_id>`
  - **Method:** PUT
  - **Description:** Updates vehicle information.
  - **Parameters:** JSON data containing fields to be updated.
  - **Response:** Message indicating successful vehicle update or error message.

#### Delete Vehicle

- **Endpoint:** `/api/vehicles/<int:vehicle_id>`
  - **Method:** DELETE
  - **Description:** Deletes a vehicle with the specified vehicle ID.
  - **Response:** Message indicating successful vehicle deletion or error message.

### View Users API

#### View All Users

- **Endpoint:** `/api/view_users`
  - **Method:** GET
  - **Description:** Retrieves information about all users.
  - **Response:** JSON data containing information about all users.

#### View User Detail

- **Endpoint:** `/api/view_users/<int:user_id>`
  - **Method:** GET
  - **Description:** Retrieves detailed information about a specific user.
  - **Response:** JSON data containing information about the specified user.

### View Vehicles API

#### View All Vehicles

- **Endpoint:** `/api/view_vehicles`
  - **Method:** GET
  - **Description:** Retrieves information about all vehicles.
  - **Response:** JSON data containing information about all vehicles.

#### View Vehicle Detail

- **Endpoint:** `/api/view_vehicles/<int:vehicle_id>`
  - **Method:** GET
  - **Description:** Retrieves detailed information about a specific vehicle.
  - **Response:** JSON data containing information about the specified vehicle.

### View Visitors API

#### View All Visitors

- **Endpoint:** `/api/view_visitors`
  - **Method:** GET
  - **Description:** Retrieves information about all visitors.
  - **Response:** JSON data containing information about all visitors.

#### View Visitor Detail

- **Endpoint:** `/api/view_visitors/<int:visitor_id>`
  - **Method:** GET
  - **Description:** Retrieves detailed information about a specific visitor.
  - **Response:** JSON data containing information about the specified visitor.

### Update User Information by OCR Scan

- **Endpoint:** `/api/update_user_by_ocr`
  - **Method:** POST
  - **Description:** Updates user information using OCR scan.
  - **Parameters:** Image file containing user information.
  - **Response:** Message indicating successful user information update or error message.

### Update Visitor Information by OCR Scan

- **Endpoint:** `/api/update_visitor_by_ocr`
  - **Method:** POST
  - **Description:** Updates visitor information using OCR scan.
  - **Parameters:** Image file containing visitor information.
  - **Response:** Message indicating successful visitor information update or error message.


Describe the structure of the database tables.

- **User Table:**
  - Fields: id, username, password_hash, role, image_path
- **Admin User Table:**
  - Fields: id, username, password_hash, role, image_path, company_name, reg_no, founded_date, address, contact_details
- ...

**EndPoins**

### User Management
- **POST /api/users**: Create a new user.
- **GET /api/users**: Retrieve all users.
- **GET /api/users/<user_id>**: Retrieve details of a specific user.
- **PUT /api/users/<user_id>**: Update user details.
- **DELETE /api/users/<user_id>**: Delete a user.

### Admin User Management
- **POST /api/admin_users**: Create a new admin user.
- **GET /api/admin_users**: Retrieve all admin users.
- **GET /api/admin_users/<user_id>**: Retrieve details of a specific admin user.
- **PUT /api/admin_users/<user_id>**: Update admin user details.
- **DELETE /api/admin_users/<user_id>**: Delete an admin user.

### Staff User Management
- **POST /api/staff_users**: Create a new staff user.
- **GET /api/staff_users**: Retrieve all staff users.
- **GET /api/staff_users/<user_id>**: Retrieve details of a specific staff user.
- **PUT /api/staff_users/<user_id>**: Update staff user details.
- **DELETE /api/staff_users/<user_id>**: Delete a staff user.

### Visitor Management
- **POST /api/visitors**: Create a new visitor.
- **GET /api/visitors**: Retrieve all visitors.
- **GET /api/visitors/<visitor_id>**: Retrieve details of a specific visitor.
- **PUT /api/visitors/<visitor_id>**: Update visitor details.
- **DELETE /api/visitors/<visitor_id>**: Delete a visitor.

### Vehicle Management
- **POST /api/vehicles**: Register a new vehicle.
- **GET /api/vehicles**: Retrieve all vehicles.
- **GET /api/vehicles/<vehicle_id>**: Retrieve details of a specific vehicle.
- **PUT /api/vehicles/<vehicle_id>**: Update vehicle details.
- **DELETE /api/vehicles/<vehicle_id>**: Delete a vehicle.

### Authentication
- **POST /api/login**: Authenticate user login.

### View Details
- **GET /api/view/users**: Retrieve all users.
- **GET /api/view/users/<user_id>**: Retrieve details of a specific user.
- **GET /api/view/vehicles**: Retrieve all vehicles.
- **GET /api/view/vehicles/<vehicle_id>**: Retrieve details of a specific vehicle.
- **GET /api/view/visitors**: Retrieve all visitors.
- **GET /api/view/visitors/<visitor_id>**: Retrieve details of a specific visitor.

### OCR-based Updates
- **POST /api/update_user_by_ocr**: Update user information using OCR.
- **POST /api/update_visitor_by_ocr**: Update visitor information using OCR.

### Company-specific Details
- **GET /api/view/visitors/company/<user_id>**: Retrieve visitors of a specific company.
- **GET /api/view/staffs/company/<user_id>**: Retrieve staffs of a specific company.

### Admin Users View
- **GET /api/view/admin_users**: Retrieve all admin users.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with any improvements or feature additions.

## Frontend Usage

Explain how to use the APIs in the frontend application.

```Front-ENd 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Frontend</title>
</head>
<body>
    <h1>User Registration Form</h1>
    <form id="userForm">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <label for="role">Role:</label>
        <select id="role" name="role">
            <option value="user">User</option>
            <option value="admin">Admin</option>
            <option value="staff">Staff</option>
        </select><br>
        <label for="imagePath">Image Path:</label>
        <input type="text" id="imagePath" name="imagePath"><br>
        <button type="submit">Register</button>
    </form>

    <script>
        document.getElementById('userForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('/api/users', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error registering user');
                }
                return response.json();
            })
            .then(data => {
                alert('User registered successfully');
                // Additional handling or redirection after successful registration
            })
            .catch(error => {
                alert('An error occurred: ' + error.message);
            });
        });
    </script>
</body>
</html>

```

## Contributing

Explain how others can contribute to the project.

## License

Specify the project's license (e.g., MIT License).

---

This README provides detailed documentation for API endpoints, database structure, frontend usage, and contribution guidelines. Adjust the information according to your project's specifications.
