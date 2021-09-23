import unittest
import requests
import pytest
from app import app


class TestApi(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

    def test_1_start(self):
        resp = requests.get(self.URL)
        r = app.test_client().get(self.URL)

        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
