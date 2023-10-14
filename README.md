# Movie API Project

This is a movie API project built with Flask and SQLite. It allows users to register, log in, and view movie information.

## Prerequisites

- Python 3.6+
- Virtual Environment

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/kunal-geeks/movie_api.git

2. Navigate to the project directory and create a virtual environment:
    ```sh
    Copy code
    cd movie_api
    python -m venv venv
    
3. Activate the virtual environment:
On Windows:
    ```sh
    Copy code
    venv\Scripts\activate
On macOS and Linux:
    ```sh
    Copy code
    source venv/bin/activate

3. Install dependencies:
    ```sh
    Copy code
    pip install -r requirements.txt

4. Create a .env file in the project root and set your ZeroBounce API key:
    makefile
    Copy code
    ZEROBOUNCE_API_KEY=your_api_key
    (Get your API key by registering at ZeroBounce)

5. Populate the SQLite database:
    ```sh
    Copy code
    python populate_db.py

6. Create _static and _templates folders inside app/docs/source folder.
    
7. Build the documentation:
    ```sh
    Copy code
    cd app/docs
    mkdir build
    sphinx-build -M html source build

8. Create admin credentials:
    ```sh
    Copy code
    python add_admin.py
    Admin credentials:

    Email: admin@example.com
    Password: admin

9. Run the application:
    ```sh
    Copy code
    flask run
Access the application in your browser: http://127.0.0.1:5000

10. Demo
For a live demo, visit https://kunal7777.pythonanywhere.com/

Admin Credentials:
Email: admin@example.com
Password: admin

11. Tests
To run tests, use pytest:
    ```sh
    Copy code
    pytest

12. To view the test coverage report:
    ```sh
    Copy code
    coverage run -m pytest
    coverage report

13. For a detailed HTML coverage report:
    ```sh
    Copy code
    coverage html
    
Open htmlcov/index.html in your browser to see the report.

License
This project is licensed under the MIT License - see the LICENSE file fordetails.





