
from config import create_app # Import the factory function and db
from extensions import db

try:
    print(f'App is attempting to run')

    if __name__ == '__main__':
        app = create_app()  # Create the app instance using the factory function
        with app.app_context():
            db.create_all()  # Create tables
            print("Tables created:")
        app.run(debug=True)

except Exception as e:
    print(f'Error is {e}')

# Update an existing blog post
# Filter blog posts by a search term
