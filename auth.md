Sure, I'll provide documentation for each API endpoint in the VVIMS API:

---

# VVIMS API Documentation

This document provides an overview of the endpoints available in the VVIMS (Visitor and Vehicle Information Management System) API.

## Authentication

**base_dir : /api/v1/auth**

### Register User

Endpoint: `/register`  
Method: POST  
Description: Register a new user with the system.  
Request Body:
- `username` (string, required): The username of the user.
- `email` (string, required): The email address of the user.
- `password` (string, required): The password of the user.

### User Login

Endpoint: `/login`  
Method: POST  
Description: Authenticate a user and generate access and refresh tokens.  
Request Body:
- `username` (string, required): The username of the user.
- `password` (string, required): The password of the user.

### Get Current User

Endpoint: `/me`  
Method: GET  
Description: Retrieve details of the currently authenticated user.  
Authorization: JWT token required in the request headers.

### Refresh Access Token

Endpoint: `/token/refresh`  
Method: GET  
Description: Refresh the access token using the refresh token.  
Authorization: JWT token required in the request headers.

## User Management

### Get All Users

Endpoint: `/all_users`  
Method: GET  
Description: Retrieve details of all users in the system.  
Authorization: JWT token required in the request headers.

### Get User by ID

Endpoint: `/user/{id}`  
Method: GET  
Description: Retrieve details of a specific user by their ID.  
Authorization: JWT token required in the request headers.

### Delete User

Endpoint: `/{id}`  
Method: DELETE  
Description: Delete a user from the system by their ID.  
Authorization: JWT token required in the request headers.

## Role-based Authorization

### Get Role
Endpoint: `/role`  
Method: GET  
Description: Retrieve the role of the current user.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff'.

---

These are the endpoints available in the VVIMS API along with their descriptions and authorization requirements. Feel free to customize this documentation further based on your project's specific needs.
