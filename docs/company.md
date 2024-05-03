
---

# Company Management API Documentation

This document provides details about the company management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.

**base url: api/v1/company**

## Company Registration

Endpoint: `/register`  
Method: POST  
Description: Register a new company along with an associated user account.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.  

### Request Body Fields:
- `username` (string): The username for the company's user account.
- `email` (string): The email address for the company's user account.
- `password` (string): The password for the company's user account.
- `company_name` (string): The name of the company.
- `tax_number` (string): The tax identification number of the company.
- `industry` (string): The industry of the company.
- `company_size` (string): The size of the company.
- `company_tel` (string): The telephone number of the company.
- `company_email` (string): The email address of the company.
- `company_gps` (string): The GPS coordinates of the company.
- `company_address` (string): The address of the company.
- `managed_by` (string): The name of the manager.
- `manager_role` (string): The role of the manager.
- `manager_tel` (string): The telephone number of the manager.
- `manager_email` (string): The email address of the manager.

## Retrieve All Companies

Endpoint: `/all_comp`  
Method: GET  
Description: Retrieve details of all registered companies.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.

### Response Body Fields:
- `id` (integer): The unique identifier of the company.
- `company_name` (string): The name of the company.
- `tax_number` (string): The tax identification number of the company.
- `industry` (string): The industry of the company.
- `company_size` (string): The size of the company.
- `company_tel` (string): The telephone number of the company.
- `company_email` (string): The email address of the company.
- `company_gps` (string): The GPS coordinates of the company.
- `company_address` (string): The address of the company.
- `managed_by` (string): The name of the manager.
- `manager_role` (string): The role of the manager.
- `manager_tel` (string): The telephone number of the manager.
- `manager_email` (string): The email address of the manager.

## Retrieve My Company

Endpoint: `/me`  
Method: GET  
Description: Retrieve details of the company associated with the currently authenticated user.  
Authorization: JWT token required in the request headers.  

### Response Body Fields:
- Same as the fields in the "Retrieve All Companies" response.

## Retrieve Company by ID

Endpoint: `/company/{id}`  
Method: GET  
Description: Retrieve details of a specific company by its ID.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.

### Response Body Fields:
- Same as the fields in the "Retrieve All Companies" response.

## Delete Company

Endpoint: `/delete_comp/{id}`  
Method: DELETE  
Description: Delete a company from the system by its ID.  
Permissions: No specific role required.

---

This documentation provides a comprehensive overview of the company management endpoints, including the fields expected in the request body and response body for each API.
