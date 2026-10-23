import unittest

from app import app


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pages_load(self):
        for path in ("/", "/menu", "/about", "/contact"):
            self.assertEqual(self.client.get(path).status_code, 200, path)

    def test_menu_filter(self):
        html = self.client.get("/menu?tag=Tea").get_data(as_text=True)
        self.assertIn("Masala Chai", html)
        self.assertNotIn("Flat White", html)

    def test_api_and_health(self):
        self.assertEqual(self.client.get("/health").get_json()["status"], "ok")
        self.assertEqual(len(self.client.get("/api/menu").get_json()), 6)

    def test_contact_validation(self):
        bad = self.client.post("/contact", data={"name": "A", "email": "nope", "message": "short"})
        self.assertEqual(bad.status_code, 400)
        good = self.client.post("/contact", data={"name": "Asha", "email": "a@b.co",
                                                  "message": "Table for four on Saturday please."})
        self.assertEqual(good.status_code, 200)
        self.assertIn("Thank you", good.get_data(as_text=True))

    def test_404(self):
        self.assertEqual(self.client.get("/nope").status_code, 404)


if __name__ == "__main__":
    unittest.main()
