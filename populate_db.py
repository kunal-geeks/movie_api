from app import create_app
from db_utils import load_data_from_json, empty_database

if __name__ == "__main__":
    json_file_path = 'imdb.json'
    app = create_app(test_config='production')  # Create an app instance without specifying a test config
    with app.app_context():
        empty_database()  # Empty the database first
        load_data_from_json(json_file_path, app)