Certainly! Here's the updated documentation with fields included for each API endpoint:

---

# Employee Management API Documentation

This document provides details about the employee management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.


**base_url : /auth/v1/emplyee**

## Employee Registration

Endpoint: `/register`  
Method: POST  
Description: Register a new employee along with a user account.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff'.  

### Request Body Fields:
- `username` (string): The username for the employee's user account.
- `email` (string): The email address for the employee's user account.
- `password` (string): The password for the employee's user account.
- `full_name` (string): The full name of the employee.
- `staff_email` (string): The email address of the employee.
- `staff_social_link` (string): The social media link of the employee.
- `staff_role` (string): The role of the employee.
- `staff_home_address` (string): The home address of the employee.
- `staff_department` (string): The department of the employee.
- `image_path` (string, optional): The image path of the employee.

## Retrieve All Employees

Endpoint: `/all_emp`  
Method: GET  
Description: Retrieve details of all registered employees.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.

### Response Body Fields:
- `id` (integer): The unique identifier of the employee.
- `full_name` (string): The full name of the employee.
- `staff_email` (string): The email address of the employee.
- `staff_social_link` (string): The social media link of the employee.
- `staff_role` (string): The role of the employee.
- `staff_home_address` (string): The home address of the employee.
- `staff_department` (string): The department of the employee.
- `image_path` (string, optional): The image path of the employee.

## Retrieve My Employee

Endpoint: `/me`  
Method: GET  
Description: Retrieve details of the employee associated with the currently authenticated user.  
Authorization: JWT token required in the request headers.  

### Response Body Fields:
- Same as the fields in the "Retrieve All Employees" response.

## Retrieve Employees of My Company

Endpoint: `/com_employees`  
Method: GET  
Description: Retrieve details of all employees associated with the company of the currently authenticated user.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff'.

### Response Body Fields:
- Same as the fields in the "Retrieve All Employees" response.

## Retrieve Employee by ID

Endpoint: `/employee/{id}`  
Method: GET  
Description: Retrieve details of a specific employee by its ID.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff'.

### Response Body Fields:
- Same as the fields in the "Retrieve All Employees" response.

## Delete Employee

Endpoint: `/delete_comp/{id}`  
Method: DELETE  
Description: Delete an employee from the system by its ID.  
Permissions: No specific role required.

---

This documentation provides a comprehensive overview of the employee management endpoints, including the fields expected in the request body and response body for each API.
