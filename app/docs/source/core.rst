Core Routes
===========

.. automodule:: app.routes.core
    :members:

Index Endpoint
--------------

.. http:get:: /

    Renders the index page.

    :statuscode 200: Rendered 'index.html' template.

Login Endpoint
--------------

.. http:get:: /login

    Renders the login page.

    :statuscode 200: Rendered 'login.html' template.

Register Endpoint
-----------------

.. http:get:: /register

    Renders the register page.

    :statuscode 200: Rendered 'register.html' template.

Dashboard Endpoint
------------------

.. http:get:: /dashboard

    Renders the dashboard page based on user authentication and admin status.

    :statuscode 200: Rendered 'admin_dashboard.html' template for admin users.
    :statuscode 200: Rendered 'user_dashboard.html' template for non-admin users.

Edit Account Endpoint
---------------------

.. http:get:: /edit-account

    Route for viewing and editing the user's account information.

    **Method:** `GET`

    **Responses:**

    - `200 OK`: Rendered 'edit_account.html' template with user's name and email.

      .. code-block:: json

         {
             "status": "success",
             "message": "User account details retrieved successfully.",
             "data": {
                 "name": "User Name",
                 "email": "user@example.com"
             }
         }

.. http:put:: /edit-account

    Route for updating the user's account information.

    **Method:** `PUT`

    **Parameters:**
    - `name` (string, optional): Updated user's name.
    - `email` (string, optional): Updated user's email address.
    - `password` (string, optional): New password.

    **Responses:**

    - `200 OK`: Password updated successfully.

      .. code-block:: json

         {
             "status": "success",
             "message": "Password updated successfully."
         }

    - `400 Bad Request`: New password is required or invalid parameters.

      .. code-block:: json

         {
             "status": "fail",
             "message": "New password is required."
         }

    - `500 Internal Server Error`: Failed to update password. Please try again.

      .. code-block:: json

         {
             "status": "fail",
             "message": "Failed to update password. Please try again."
         }
