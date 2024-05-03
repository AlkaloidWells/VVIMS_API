Here is the detailed documentation for the APIs in the Sadmin Blueprint:

# Sadmin API Documentation

## Register Super Admin Endpoint

### Register Super Admin
- **URL:**  `/api/v1/sadmin/register` 
- **Method:** POST
- **Description:** Register a new super admin with the provided details.
- **Request Body:**
  -  `username` : Super admin's username
  -  `email` : Super admin's email address
  -  `password` : Super admin's password
  -  `full_name` : Super admin's full name
- **Response:**
  -  `HTTP_201_CREATED` : Super admin created successfully
  -  `HTTP_400_BAD_REQUEST` : Bad request due to validation errors
  -  `HTTP_409_CONFLICT` : Email or username already taken

## Super Admin Management Endpoints

### Delete Super Admin
- **URL:**  `/api/v1/sadmin/delete_samin/<int:sadmin_id>` 
- **Method:** DELETE
- **Description:** Delete a super admin by ID.
- **Response:**
  -  `HTTP_200_OK` : Super admin deleted successfully
  -  `HTTP_404_NOT_FOUND` : Super admin not found

### Update Super Admin Image
- **URL:**  `/api/v1/sadmin/update_image/<int:ad_id>` 
- **Method:** PUT
- **Description:** Update super admin's image by super admin ID.
- **Response:**
  -  `HTTP_200_OK` : Super admin image updated successfully
  -  `HTTP_400_BAD_REQUEST` : No file or selected file error
  -  `HTTP_404_NOT_FOUND` : Super admin not found
  -  `HTTP_500_INTERNAL_SERVER_ERROR` : Internal server error

### Get Super Admin Image
- **URL:**  `/api/v1/sadmin/get_com_image/<int:ad_id>` 
- **Method:** GET
- **Description:** Get super admin's image by super admin ID.
- **Response:**
  -  `HTTP_200_OK` : Super admin image path retrieved successfully
  -  `HTTP_404_NOT_FOUND` : Super admin does not have an image

This documentation provides a detailed overview of the sadmin API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.