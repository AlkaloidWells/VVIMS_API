Certainly! Here's the updated documentation with fields included for each API endpoint:

---

# Employee Management API Documentation

This document provides details about the employee management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.


**base_url : /auth/v1/emplyee**

# Employee API Documentation 
 
## Employee Registration Endpoints 
 
### Register Employee 
- **URL:**  /api/v1/employee/register  
- **Method:** POST 
- **Description:** Register a new employee with the provided details. 
- **Request Body:** 
  -  username : Employee's username 
  -  email : Employee's email address 
  -  password : Employee's password 
  -  full_name : Employee's full name 
  -  staff_email : Employee's staff email 
  -  staff_social_link : Employee's social media link 
  -  staff_role : Employee's role 
  -  staff_home_address : Employee's home address 
  -  staff_department : Employee's department 
  -  image_path  (Optional): Employee's image path 
- **Response:** 
  -  HTTP_201_CREATED : Employee created successfully 
  -  HTTP_400_BAD_REQUEST : Bad request due to validation errors 
  -  HTTP_409_CONFLICT : Email or username already taken 
 
### Register Employee by ID 
- **URL:**  /api/v1/employee/register/<int:comp_id>  
- **Method:** POST 
- **Description:** Register a new employee with the provided details associated with a specific company ID. 
- **Request Body:** 
  - Same as Register Employee endpoint 
- **Response:** 
  - Same as Register Employee endpoint 
 
## Employee Management Endpoints 
 
### Get All Employees 
- **URL:**  /api/v1/employee/all_emp  
- **Method:** GET 
- **Description:** Retrieve details of all employees (accessible to super admin). 
- **Response:** 
  -  HTTP_200_OK : List of all employees retrieved successfully 
 
### Get My Employee 
- **URL:**  /api/v1/employee/me  
- **Method:** GET 
- **Description:** Get details of the logged-in user's employee. 
- **Response:** 
  -  HTTP_200_OK : Employee details retrieved successfully 
  -  HTTP_404_NOT_FOUND : Employee not found 
 
### Get Company Employees 
- **URL:**  /api/v1/employee/com_employees  
- **Method:** GET 
- **Description:** Get details of all employees associated with the current user's company. 
- **Response:** 
  -  HTTP_200_OK : List of company employees retrieved successfully 
  -  HTTP_404_NOT_FOUND : No employees found for the company 
 
### Get Employee by ID 
- **URL:**  /api/v1/employee/employee/<int:id>  
- **Method:** GET 
- **Description:** Retrieve employee details by employee ID (accessible to super admin or company role). 
- **Response:** 
  -  HTTP_200_OK : Employee details retrieved successfully 
  -  HTTP_404_NOT_FOUND : Employee not found 
 
### Delete Employee 
- **URL:**  /api/v1/employee/delete_emp/<int:emp_id>  
- **Method:** DELETE 
- **Description:** Delete an employee by ID (accessible to super admin, company, or staff). 
- **Response:** 
  -  HTTP_200_OK : Employee deleted successfully 
  -  HTTP_404_NOT_FOUND : Employee not found 
 
### Update Employee Details 
- **URL:**  /api/v1/employee/edit_emp/<int:emp_id>  
- **Method:** PUT/PATCH 
- **Description:** Update employee details by employee ID (accessible to super admin, company, or staff). 
- **Response:** 
  -  HTTP_200_OK : Employee details updated successfully 
  -  HTTP_404_NOT_FOUND : Employee not found 
 
### Update Employee Image 
- **URL:**  /api/v1/employee/update_image/<int:emp_id>  
- **Method:** PUT 
- **Description:** Update employee's image by employee ID (accessible to staff). 
- **Response:** 
  -  HTTP_200_OK : Employee image updated successfully 
  -  HTTP_400_BAD_REQUEST : No file or selected file error 
  -  HTTP_404_NOT_FOUND : Employee not found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Get Employee Image 
- **URL:**  /api/v1/employee/get_com_image/<int:emp_id>  
- **Method:** GET 
- **Description:** Get employee's image by employee ID. 
- **Response:** 
  -  HTTP_200_OK : Employee image path retrieved successfully 
  -  HTTP_404_NOT_FOUND : Employee does not have an image 
 
### Search Employees 
- **URL:**  /api/v1/employee/emp_search  
- **Method:** POST 
- **Description:** Search for employees by any attribute (accessible to super admin, company, staff, user). 
- **Response:** 
  -  HTTP_200_OK : List of employees matching the search criteria 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
This README provides a detailed overview of the employee API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.