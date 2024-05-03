Here's the documentation for the visitor management API with the fields included for each endpoint:

---

# Visitor Management API Documentation

This document provides details about the visitor management endpoints in the VVIMS (Visitor and Vehicle Information Management System) API.

**base_url : /auth/v1/visitor**
  
## Register Visitor Endpoints 
 
### Register Visitor by Company ID 
- **URL:**  /api/v1/visitor/register/<int:comp_id>  
- **Method:** POST 
- **Description:** Register a new visitor associated with a specific company ID. 
- **Request Body:** 
  -  full_name : Visitor's full name 
  -  address : Visitor's address 
  -  contact_details : Visitor's contact details 
  -  purpose_of_visit : Purpose of the visit 
  -  time_in : Time of entry 
  -  badge_issued : Badge issued status 
- **Response:** 
  -  HTTP_201_CREATED : Visitor created successfully 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Register Visitor 
- **URL:**  /api/v1/visitor/register  
- **Method:** POST 
- **Description:** Register a new visitor with associated user's company ID. 
- **Request Body:** 
  - Same as Register Visitor by Company ID 
- **Response:** 
  - Same as Register Visitor by Company ID 
 
## Visitor Management Endpoints 
 
### Delete Visitor 
- **URL:**  /api/v1/visitor/delete/<int:visitor_id>  
- **Method:** DELETE 
- **Description:** Delete a visitor by ID (accessible to super admin, company, or staff). 
- **Response:** 
  -  HTTP_204_NO_CONTENT : Visitor deleted successfully 
  -  HTTP_404_NOT_FOUND : Visitor not found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Update Visitor 
- **URL:**  /api/v1/visitor/update/<int:visitor_id>  
- **Method:** PUT 
- **Description:** Update visitor details by visitor ID (accessible to super admin, company, or staff). 
- **Response:** 
  -  HTTP_200_OK : Visitor updated successfully 
  -  HTTP_404_NOT_FOUND : Visitor not found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Register Visitor Card 
- **URL:**  /api/v1/visitor/register_card  
- **Method:** POST 
- **Description:** Register a visitor card with personal details. 
- **Request Body:** 
  -  surname : Visitor's surname 
  -  given_name : Visitor's given name 
  -  dob : Visitor's date of birth 
  -  pob : Visitor's place of birth 
  -  sex : Visitor's gender 
  -  proff : Visitor's profession 
  -  id_card_number : Visitor's ID card number 
- **Response:** 
  -  HTTP_201_CREATED : Visitor card registered successfully 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Update Visitor Card 
- **URL:**  /api/v1/visitor/update_card/<int:visitor_id>  
- **Method:** PUT 
- **Description:** Update visitor card details by visitor ID (accessible to super admin, company, or staff). 
- **Response:** 
  -  HTTP_200_OK : Visitor card updated successfully 
  -  HTTP_404_NOT_FOUND : Visitor not found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
## Search Endpoints 
 
### Search Visitors 
- **URL:**  /api/v1/visitor/vic_search  
- **Method:** POST 
- **Description:** Search for visitors by any attribute (accessible to super admin, company, staff, user). 
- **Response:** 
  -  HTTP_200_OK : List of visitors matching the search criteria 
  -  HTTP_404_NOT_FOUND : No visitors found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
### Search Visitor Cards 
- **URL:**  /api/v1/visitor/search_card  
- **Method:** POST 
- **Description:** Search for visitor cards by any attribute (accessible to super admin, company, staff, user). 
- **Response:** 
  -  HTTP_200_OK : List of visitor cards matching the search criteria 
  -  HTTP_404_NOT_FOUND : No visitor cards found 
  -  HTTP_500_INTERNAL_SERVER_ERROR : Internal server error 
 
This documentation provides a detailed overview of the visitor API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.