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
    cd movie_api
    python -m venv venv
    
3. Activate the virtual environment:
- On Windows:
    ```sh
    venv\Scripts\activate
- On macOS and Linux:
    ```sh
    source venv/bin/activate

4. Install dependencies:
    ```sh
    pip install -r requirements.txt

5. Create a .env file in the project root and set your ZeroBounce API key:


- ZEROBOUNCE_API_KEY=your_api_key
- Get your API key by registering at https://www.zerobounce.net/members/signin

6. Populate the SQLite database:
    ```sh
    python populate_db.py

7. Create _static and _templates folders inside app/docs/source folder.
    
8. Build the documentation:
    ```sh
    cd app/docs
    mkdir build
    sphinx-build -M html source build

9. Create admin credentials:
    ```sh
    python add_admin.py

Admin credentials:
- Email: admin@example.com
- Password: admin

10. Run the application:
    ```sh
    flask run

- Access the application in your browser: http://127.0.0.1:5000

11. Demo
For a live demo, visit https://kunal7777.pythonanywhere.com/

Admin Credentials:

- Email: admin@example.com
- Password: admin

User Credentials: you can register with valid email id

12. Tests
To run tests, use pytest:
    ```sh
    pytest

13. To view the test coverage report:
    ```sh
    coverage run -m pytest
    coverage report

14. For a detailed HTML coverage report:
    ```sh
    coverage html

Open htmlcov/index.html in your browser to see the report.

License
This project is licensed under the MIT License - see the LICENSE file fordetails.





