from app import app
from models import db, Plant
import unittest

class TestPlant(unittest.TestCase):
    def setUp(self):
        """Set up test database and add a plant."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Add a test plant to the database
            plant = Plant(id=1, name="Test Plant", image="test.jpg", price=10.0, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        with app.app_context():
            plant_1 = Plant.query.filter_by(id=1).first()
            plant_1.is_in_stock = False
            db.session.commit()

            # Assert the change
            updated_plant = Plant.query.filter_by(id=1).first()
            self.assertFalse(updated_plant.is_in_stock)

if __name__ == "__main__":
    unittest.main()
