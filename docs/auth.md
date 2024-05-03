Sure, I'll provide documentation for each API endpoint in the VVIMS API:

---

# VVIMS API Documentation

This document provides an overview of the endpoints available in the VVIMS (Visitor and Vehicle Information Management System) API.

## Authentication

**base_dir : /api/v1/auth**

## Authentication Endpoints 
 
### Register User 
- **URL:**  /api/v1/auth/register  
- **Method:** POST 
- **Description:** Register a new user with the provided details. 
- **Request Body:** 
  -  username : User's username 
  -  email : User's email address 
  -  role : User's role 
  -  password : User's password 
- **Response:** 
  -  HTTP_201_CREATED : User created successfully 
  -  HTTP_400_BAD_REQUEST : Bad request due to validation errors 
  -  HTTP_409_CONFLICT : Email or username already taken 
 
### Login User 
- **URL:**  /api/v1/auth/login  
- **Method:** POST 
- **Description:** Authenticate user credentials and generate access and refresh tokens. 
- **Request Body:** 
  -  username : User's username 
  -  password : User's password 
- **Response:** 
  -  HTTP_200_OK : User logged in successfully 
  -  HTTP_401_UNAUTHORIZED : Wrong credentials provided 
 
### Get Current User Details 
- **URL:**  /api/v1/auth/me  
- **Method:** GET 
- **Description:** Get details of the currently logged-in user. 
- **Response:** 
  -  HTTP_200_OK : User details retrieved successfully 
 
### Refresh User Token 
- **URL:**  /api/v1/auth/token/refresh  
- **Method:** GET 
- **Description:** Refresh the user's access token using the refresh token. 
- **Response:** 
  -  HTTP_200_OK : Token refreshed successfully 
 
### Get All Users 
- **URL:**  /api/v1/auth/all_users  
- **Method:** GET 
- **Description:** Retrieve details of all users (only accessible to super admin). 
- **Response:** 
  -  HTTP_200_OK : List of all users retrieved successfully 
 
### Get User by ID 
- **URL:**  /api/v1/auth/user/<int:id>  
- **Method:** GET 
- **Description:** Retrieve user details by user ID (only accessible to super admin). 
- **Response:** 
  -  HTTP_200_OK : User details retrieved successfully 
  -  HTTP_404_NOT_FOUND : User not found 
 
### Delete User 
- **URL:**  /api/v1/auth/<int:id>  
- **Method:** DELETE 
- **Description:** Delete a user by ID (only accessible to super admin). 
- **Response:** 
  -  HTTP_204_NO_CONTENT : User deleted successfully 
  -  HTTP_404_NOT_FOUND : User not found 
 
### Get User Role 
- **URL:**  /api/v1/auth/role  
- **Method:** GET 
- **Description:** Get the role of the current user (only accessible to company role). 
- **Response:** 
  -  HTTP_200_OK : User role retrieved successfully 
 
### Change User Password 
- **URL:**  /api/v1/auth/change_password/<string:user_email>  
- **Method:** PUT 
- **Description:** Change the password of a user by email address. 
- **Request Body:** 
  -  new_password : New password for the user 
- **Response:** 
  -  HTTP_200_OK : User password changed successfully 
  -  HTTP_400_BAD_REQUEST : New password not provided 
  -  HTTP_404_NOT_FOUND : User not found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
This README provides a detailed overview of the authentication API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.