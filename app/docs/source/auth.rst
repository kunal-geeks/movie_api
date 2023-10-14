Authentication Endpoints
=========================

.. toctree::
   :maxdepth: 1

/auth/register
--------------

Registers a user with the provided information.

**Method:** `POST`

**Parameters:**
- `name` (string): User's name.
- `email` (string): User's email address.
- `password` (string): User's password.

**Responses:**

- `201 Created`: Successfully registered. Returns an authentication token.

  .. code-block:: json

     {
         "status": "success",
         "message": "Successfully registered.",
         "auth_token": "your_auth_token_here"
     }

- `400 Bad Request`: Invalid email address.

  .. code-block:: json

     {
         "status": "fail",
         "message": "Invalid email address."
     }

- `202 Accepted`: User already exists. Please log in.

  .. code-block:: json

     {
         "status": "fail",
         "message": "User already exists. Please Log in."
     }

- `400 Bad Request`: Email address is already registered. Please use a different email.

  .. code-block:: json

     {
         "status": "fail",
         "message": "Email address is already registered. Please use a different email."
     }

- `500 Internal Server Error`: Some error occurred. Please try again.

  .. code-block:: json

     {
         "status": "fail",
         "message": "Some error occurred. Please try again."
     }


/auth/login
-----------

Logs in a user by authenticating their credentials and generates an authentication token.

**Method:** `POST`

**Parameters:**
- `email` (string): User's email address.
- `password` (string): User's password.

**Responses:**

- `200 OK`: Successfully logged in. Returns an authentication token.

  .. code-block:: json

     {
         "status": "success",
         "message": "Successfully logged in.",
         "auth_token": "your_auth_token_here"
     }

- `400 Bad Request`: Incorrect password.

  .. code-block:: json

     {
         "status": "fail",
         "message": "Incorrect password."
     }

- `404 Not Found`: User does not exist.

  .. code-block:: json

     {
         "status": "fail",
         "message": "User does not exist."
     }

- `500 Internal Server Error`: Some error occurred. Please try again.

  .. code-block:: json

     {
         "status": "fail",
         "message": "Some error occurred. Please try again."
     }


/auth/status
------------

Retrieves the status of the authentication.

**Method:** `GET`

**Authentication:** Requires a valid authentication token.

**Responses:**

- `200 OK`: Successfully authenticated. Returns user information.

  .. code-block:: json

     {
         "status": "success",
         "data": {
             "user_id": 1,
             "username": "example_user",
             "email": "user@example.com",
             "admin": false,
             "registered_on": "2023-01-01T00:00:00Z"
         }
     }

- `401 Unauthorized`: Provide a valid auth token.

  .. code-block:: json

     {
         "status": "fail",
         "message": "Provide a valid auth token."
     }


/auth/logout
------------

Logs out the current user by invalidating their authentication token.

**Method:** `POST`

**Authentication:** Requires a valid authentication token.

**Responses:**

- `200 OK`: Successfully logged out.

  .. code-block:: json

     {
         "message": "Successfully logged out"
     }

- `401 Unauthorized`: No valid auth token found.

  .. code-block:: json

     {
         "message": "No valid auth token found"
     }

- `500 Internal Server Error`: An error occurred while processing your request.

  .. code-block:: json

     {
         "message": "An error occurred while processing your request"
     }
