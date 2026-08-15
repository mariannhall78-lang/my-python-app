import unittest

from app import app


class TemplateRenderingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_dashboard_renders_metrics_and_charts(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Total Products", html)
        self.assertIn("Total Categories", html)
        self.assertIn("Recent Products", html)
        self.assertIn("categoryBarChart", html)
        self.assertIn("categoryPieChart", html)
        self.assertIn("Browse Products", html)
        self.assertIn("Use Barcode Scanner", html)

    def test_supporting_pages_render_dashboard_layout(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Browse Products", response.get_data(as_text=True))

        response = self.client.get("/products/add")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Add Product", response.get_data(as_text=True))

        response = self.client.get("/scan")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Barcode Scanner", response.get_data(as_text=True))

        response = self.client.get("/products/5000112637922")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product Detail", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
