
---

# Company Management API Documentation

This document provides details about the company management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.

**base url: api/v1/company**

## Company Registration Endpoint 
 
### Register Company 
- **URL:**  /api/v1/company/register  
- **Method:** POST 
- **Description:** Register a new company with the provided details. 
- **Request Body:** 
  -  username : User's username 
  -  email : User's email address 
  -  password : User's password 
  -  company_name : Company's name 
  -  tax_number : Company's tax number 
  -  industry : Company's industry 
  -  company_size : Company's size 
  -  company_tel : Company's telephone number 
  -  company_email : Company's email 
  -  company_gps : Company's GPS location 
  -  company_address : Company's address 
  -  managed_by : Manager's name 
  -  manager_role : Manager's role 
  -  manager_tel : Manager's telephone number 
  -  manager_email : Manager's email 
- **Response:** 
  -  HTTP_201_CREATED : Company created successfully 
  -  HTTP_400_BAD_REQUEST : Bad request due to validation errors 
  -  HTTP_409_CONFLICT : Email, username, or tax number already taken 
 
## Company Management Endpoints 
 
### Get All Companies 
- **URL:**  /api/v1/company/all_comp  
- **Method:** GET 
- **Description:** Retrieve details of all companies (accessible to super admin). 
- **Response:** 
  -  HTTP_200_OK : List of all companies retrieved successfully 
 
### Get My Company 
- **URL:**  /api/v1/company/me  
- **Method:** GET 
- **Description:** Get details of the logged-in user's company. 
- **Response:** 
  -  HTTP_200_OK : Company details retrieved successfully 
  -  HTTP_404_NOT_FOUND : Company not found 
 
### Get Company by ID 
- **URL:**  /api/v1/company/company/<int:id>  
- **Method:** GET 
- **Description:** Retrieve company details by company ID (accessible to super admin). 
- **Response:** 
  -  HTTP_200_OK : Company details retrieved successfully 
  -  HTTP_404_NOT_FOUND : Company not found 
 
### Delete Company 
- **URL:**  /api/v1/company/delete_comp/<int:comp_id>  
- **Method:** DELETE 
- **Description:** Delete a company by ID (accessible to super admin or company role). 
- **Response:** 
  -  HTTP_200_OK : Company deleted successfully 
  -  HTTP_404_NOT_FOUND : Company not found 
 
### Update Company Details 
- **URL:**  /api/v1/company/edit_comp/<int:com_id>  
- **Method:** PUT/PATCH 
- **Description:** Update company details by company ID (accessible to super admin or company role). 
- **Response:** 
  -  HTTP_200_OK : Company details updated successfully 
  -  HTTP_404_NOT_FOUND : Company not found 
 
### Update Company Image 
- **URL:**  /api/v1/company/update_image/<int:user_id>  
- **Method:** PUT 
- **Description:** Update company's image by company ID (accessible to company role). 
- **Response:** 
  -  HTTP_200_OK : Company image updated successfully 
  -  HTTP_400_BAD_REQUEST : No file or selected file error 
  -  HTTP_404_NOT_FOUND : Company not found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Get Company Image 
- **URL:**  /api/v1/company/get_com_image/<int:comp_id>  
- **Method:** GET 
- **Description:** Get company's image by company ID. 
- **Response:** 
  -  HTTP_200_OK : Company image path retrieved successfully 
  -  HTTP_404_NOT_FOUND : Company does not have an image 
 
### Search Companies 
- **URL:**  /api/v1/company/company_search  
- **Method:** GET 
- **Description:** Search for companies by any attribute (accessible to super admin). 
- **Response:** 
  -  HTTP_200_OK : List of companies matching the search criteria 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
This README provides a detailed overview of the company API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.