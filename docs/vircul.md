Here is the detailed documentation for the APIs in the Vircul Blueprint:

# Vircul API Documentation

## Register Vehicle Endpoints

### Register Vehicle
- **URL:**  `/api/v1/vircul/register` 
- **Method:** POST
- **Description:** Register a new vehicle with the provided details.
- **Request Body:**
  -  `plate_number` : Vehicle's plate number
  -  `make` : Vehicle's make
  -  `model` : Vehicle's model
  -  `color` : Vehicle's color
  -  `owner_details` : Vehicle owner's details
  -  `entry_time` : Entry time of the vehicle
  -  `exit_time`  (Optional): Exit time of the vehicle
  -  `flagged_as_suspicious`  (Optional): Flagged as suspicious status
- **Response:**
  -  `HTTP_201_CREATED` : Vehicle created successfully
  -  `HTTP_400_BAD_REQUEST` : Bad request due to missing required fields
  -  `HTTP_500_INTERNAL_SERVER_ERROR` : Internal server error

### Register Vehicle by Company ID
- **URL:**  `/api/v1/vircul/register/<int:vic_id>` 
- **Method:** POST
- **Description:** Register a new vehicle associated with a specific company ID.
- **Request Body:**
  - Same as Register Vehicle
- **Response:**
  - Same as Register Vehicle

## Vehicle Management Endpoints

### Get Vehicle by ID
- **URL:**  `/api/v1/vircul/<int:vircul_id>` 
- **Method:** GET
- **Description:** Retrieve vehicle details by vehicle ID.
- **Response:**
  -  `HTTP_200_OK` : Vehicle details retrieved successfully
  -  `HTTP_404_NOT_FOUND` : Vehicle not found

### Get All Vehicles
- **URL:**  `/api/v1/vircul/all_vec` 
- **Method:** GET
- **Description:** Retrieve details of all vehicles (accessible to super admin).
- **Response:**
  -  `HTTP_200_OK` : List of all vehicles retrieved successfully

### Delete Vehicle
- **URL:**  `/api/v1/vircul/delete_vic/<int:vircul_id>` 
- **Method:** DELETE
- **Description:** Delete a vehicle by ID.
- **Response:**
  -  `HTTP_200_OK` : Vehicle deleted successfully
  -  `HTTP_404_NOT_FOUND` : Vehicle not found

### Update Vehicle
- **URL:**  `/api/v1/vircul/update_vec/<int:vircul_id>` 
- **Method:** PUT
- **Description:** Update vehicle details by vehicle ID.
- **Response:**
  -  `HTTP_200_OK` : Vehicle updated successfully
  -  `HTTP_404_NOT_FOUND` : Vehicle not found

### Get Vehicles by Company
- **URL:**  `/api/v1/vircul/by_company/<int:com_id>` 
- **Method:** GET
- **Description:** Retrieve details of vehicles associated with a specific company.
- **Response:**
  -  `HTTP_200_OK` : List of vehicles for the company retrieved successfully
  -  `HTTP_404_NOT_FOUND` : No vehicles found for the company

This documentation provides a detailed overview of the vircul API endpoints and their functionalities. Feel free to expand on each section with additional details if needed.