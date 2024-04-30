Certainly! Here's the documentation for the company-related endpoints in the VVIMS API:

---

# Company Management API Documentation

This document provides details about the company management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.

**base url: api/v1/company**


## Company Registration

Endpoint: `/register`  
Method: POST  
Description: Register a new company along with a user account.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.  

## Retrieve All Companies

Endpoint: `/all_comp`  
Method: GET  
Description: Retrieve details of all registered companies.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.

## Retrieve My Company

Endpoint: `/me`  
Method: GET  
Description: Retrieve details of the company associated with the currently authenticated user.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff'.

## Retrieve Company by ID

Endpoint: `/company/{id}`  
Method: GET  
Description: Retrieve details of a specific company by its ID.  
Authorization: JWT token required in the request headers.  
Permissions: Only accessible to users with roles other than 'staff' and 'company'.

## Delete Company

Endpoint: `/delete_comp/{id}`  
Method: DELETE  
Description: Delete a company from the system by its ID.  
Permissions: No specific role required.

---

These endpoints allow for the management of companies within the VVIMS system. Feel free to customize this documentation further based on your project's specific requirements.
