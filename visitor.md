Here's the documentation for the visitor management API with the fields included for each endpoint:

---

# Visitor Management API Documentation

This document provides details about the visitor management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.

**base_url : /auth/v1/visitor**
  
## Register New Visitor

Endpoint: `/register`  
Method: POST  
Description: Register a new visitor entry.  
Authorization: JWT token required in the request headers.  

### Request Body Fields:
- `full_name` (string): Full name of the visitor.
- `id_card_number` (string): ID card number of the visitor.
- `date_of_birth` (string): Date of birth of the visitor.
- `address` (string): Address of the visitor.
- `contact_details` (string): Contact details of the visitor.
- `purpose_of_visit` (string): Purpose of the visit.
- `time_in` (string): Time of entry of the visitor.
- `badge_issued` (boolean): Indicates if a visitor badge has been issued.

## Delete Visitor

Endpoint: `/delete_vis/{id}`  
Method: DELETE  
Description: Delete a visitor entry by its ID.  
Authorization: JWT token required in the request headers.  

## View All Visitors

Endpoint: `/all_visitors`  
Method: GET  
Description: Retrieve details of all registered visitors.  
Authorization: JWT token required in the request headers.  

### Response Body Fields:
- `id` (integer): Unique identifier of the visitor.
- `com_id` (integer): Company ID associated with the visitor.
- `full_name` (string): Full name of the visitor.
- `id_card_number` (string): ID card number of the visitor.
- `date_of_birth` (string): Date of birth of the visitor.
- `address` (string): Address of the visitor.
- `contact_details` (string): Contact details of the visitor.
- `purpose_of_visit` (string): Purpose of the visit.
- `time_in` (string): Time of entry of the visitor.
- `badge_issued` (boolean): Indicates if a visitor badge has been issued.

## View Visitor Detail by ID

Endpoint: `/visitor/{visitor_id}`  
Method: GET  
Description: Retrieve details of a specific visitor by its ID.  

## View Visitors by Company ID

Endpoint: `/by_company/{company_id}`  
Method: GET  
Description: Retrieve details of visitors associated with a specific company.  

## Update Visitor

Endpoint: `/update_vis/{visitor_id}`  
Method: PUT  
Description: Update details of a specific visitor by its ID.  

### Request Body Fields:
- Same as the fields in the "Register New Visitor" request body.

---

This documentation provides comprehensive details about the visitor management endpoints, including the fields expected in the request body and response body for each API.
