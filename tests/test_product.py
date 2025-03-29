import unittest
from app import create_app
from models.database import db

class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        response = self.client.post("/api/products", json={"name": "Laptop", "price": 1200.0})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Laptop", str(response.data))

    def test_get_all_products(self):
        self.client.post("/api/products", json={"name": "Laptop", "price": 1200.0})
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop", str(response.data))

    def test_get_single_product(self):
        self.client.post("/api/products", json={"name": "Laptop", "price": 1200.0})
        response = self.client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop", str(response.data))

    def test_update_product(self):
        self.client.post("/api/products", json={"name": "Laptop", "price": 1200.0})
        response = self.client.put("/api/products/1", json={"name": "Desktop"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Desktop", str(response.data))

    def test_delete_product(self):
        self.client.post("/api/products", json={"name": "Laptop", "price": 1200.0})
        response = self.client.delete("/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product deleted successfully", str(response.data))

if __name__ == "__main__":
    unittest.main()
