"""Main function that runs an instance of an app."""
from app import create_app


if __name__ == '__main__':
    # create an app instance and run on 5000
    app = create_app()
    app.run(host='0.0.0.0')
