"""Import statements."""
import nose
from flask_testing import TestCase
from models.bucketlist_model import app, db


class BaseTestCase(TestCase):
    """Base configurations for the tests."""

    def create_app(self):
        """Set config options for the test app."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy test db at end of tests."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    nose.run()
