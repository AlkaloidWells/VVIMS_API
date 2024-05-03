Here is the detailed documentation for the APIs in the User1 Blueprint:

# User1 API Documentation

## Register User Endpoints

### Register User by Company ID
- **URL:**  `/api/v1/user/register/<int:comp_id>` 
- **Method:** POST
- **Description:** Register a new user associated with a specific company ID.
- **Request Body:**
  -  `username` : User's username
  -  `email` : User's email address
  -  `password` : User's password
  -  `full_name` : User's full name
  -  `work_role` : User's work role
- **Response:**
  -  `HTTP_201_CREATED` : User created successfully
  -  `HTTP_400_BAD_REQUEST` : Bad request due to validation errors
  -  `HTTP_409_CONFLICT` : Email or username already taken

### Register User
- **URL:**  `/api/v1/user/register` 
- **Method:** POST
- **Description:** Register a new user with associated user's company ID.
- **Request Body:**
  - Same as Register User by Company ID
- **Response:**
  - Same as Register User by Company ID

## User Management Endpoints

### Delete User
- **URL:**  `/api/v1/user/delete_samin/<int:user_id>` 
- **Method:** DELETE
- **Description:** Delete a user by ID (accessible to super admin or user1 role).
- **Response:**
  -  `HTTP_200_OK` : User deleted successfully
  -  `HTTP_404_NOT_FOUND` : User not found

### Update User Image
- **URL:**  `/api/v1/user/update_image/<int:u_id>` 
- **Method:** PUT
- **Description:** Update user's image by user ID (accessible to user1 role).
- **Response:**
  -  `HTTP_200_OK` : User image updated successfully
  -  `HTTP_400_BAD_REQUEST` : No file or selected file error
  -  `HTTP_404_NOT_FOUND` : User not found
  -  `HTTP_500_INTERNAL_SERVER_ERROR` : Internal server error

### Get User Image
- **URL:**  `/api/v1/user/get_com_image/<int:u_id>` 
- **Method:** GET
- **Description:** Get user's image by user ID.
- **Response:**
  -  `HTTP_200_OK` : User image path retrieved successfully
  -  `HTTP_404_NOT_FOUND` : User does not have an image

This documentation provides a detailed overview of the user1 API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.