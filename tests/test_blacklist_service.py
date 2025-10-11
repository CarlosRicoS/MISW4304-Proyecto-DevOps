import unittest
import json
from datetime import datetime
from src.app import create_app
from src.infrastructure.models import db, BlacklistModel
from unittest.mock import patch


class TestBlacklistService(unittest.TestCase):
    """Test cases for blacklist service"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Create tables
        db.create_all()

        # Obtain a valid JWT once for all tests
        token_resp = self.client.post('/token')
        token_data = json.loads(token_resp.data)
        self.auth_headers = {
            "Authorization": f"Bearer {token_data['token']}",
            "Content-Type": "application/json"
        }
        self.auth_only_headers = {
            "Authorization": f"Bearer {token_data['token']}"
        }

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_email_to_blacklist_success(self):
        """Test successfully adding an email to blacklist"""
        data = {
            "email": "test@example.com",
            "app_uuid": "12345678-1234-1234-1234-123456789012",
            "blocked_reason": "Spam detected"
        }

        response = self.client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=self.auth_headers
        )

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn("mensaje", response_data)
        self.assertEqual(response_data["email"], "test@example.com")

    def test_add_duplicate_email_to_blacklist(self):
        """Test adding duplicate email to blacklist"""
        data = {
            "email": "test@example.com",
            "app_uuid": "12345678-1234-1234-1234-123456789012",
            "blocked_reason": "Spam detected"
        }

        self.client.post('/blacklists', data=json.dumps(data), headers=self.auth_headers)
        response = self.client.post('/blacklists', data=json.dumps(data), headers=self.auth_headers)

        self.assertEqual(response.status_code, 409)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)

    def test_check_blacklisted_email(self):
        """Test checking if an email is blacklisted"""
        blacklist_entry = BlacklistModel(
            email="blacklisted@example.com",
            app_uuid="12345678-1234-1234-1234-123456789012",
            blocked_reason="Spam detected",
            created_at=datetime.utcnow()
        )
        db.session.add(blacklist_entry)
        db.session.commit()

        response = self.client.get('/blacklists/blacklisted@example.com', headers=self.auth_only_headers)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data["blacklisted"])
        self.assertEqual(response_data["email"], "blacklisted@example.com")
        self.assertEqual(response_data["blocked_reason"], "Spam detected")

    def test_check_non_blacklisted_email(self):
        """Test checking if a non-blacklisted email"""
        response = self.client.get('/blacklists/clean@example.com', headers=self.auth_only_headers)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertFalse(response_data["blacklisted"])
        self.assertEqual(response_data["email"], "clean@example.com")

    def test_missing_authorization_header(self):
        """Test request without authorization header"""
        data = {
            "email": "test@example.com",
            "app_uuid": "12345678-1234-1234-1234-123456789012",
            "blocked_reason": "Spam detected"
        }

        response = self.client.post(
            '/blacklists',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_invalid_email_format(self):
        """Test adding invalid email format"""
        data = {
            "email": "invalid-email",
            "app_uuid": "12345678-1234-1234-1234-123456789012",
            "blocked_reason": "Spam detected"
        }

        response = self.client.post('/blacklists', data=json.dumps(data), headers=self.auth_headers)

        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()