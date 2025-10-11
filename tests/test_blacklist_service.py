import unittest
import json
from datetime import datetime
from src.app import create_app
from src.infrastructure.models import db, BlacklistModel


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
        
        headers = {
            "Authorization": "Bearer test-token",
            "Content-Type": "application/json"
        }
        
        response = self.client.post('/blacklists', 
                                    data=json.dumps(data), 
                                    headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn("mensaje", response_data)
        self.assertEqual(response_data["email"], "test@example.com")

    def test_add_duplicate_email_to_blacklist(self):
        """Test adding duplicate email to blacklist"""
        # First add
        data = {
            "email": "test@example.com",
            "app_uuid": "12345678-1234-1234-1234-123456789012",
            "blocked_reason": "Spam detected"
        }
        
        headers = {
            "Authorization": "Bearer test-token",
            "Content-Type": "application/json"
        }
        
        self.client.post('/blacklists', 
                        data=json.dumps(data), 
                        headers=headers)
        
        # Try to add again
        response = self.client.post('/blacklists', 
                                    data=json.dumps(data), 
                                    headers=headers)
        
        self.assertEqual(response.status_code, 409)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)

    def test_check_blacklisted_email(self):
        """Test checking if an email is blacklisted"""
        # First add email to blacklist
        blacklist_entry = BlacklistModel(
            email="blacklisted@example.com",
            app_uuid="12345678-1234-1234-1234-123456789012",
            blocked_reason="Spam detected",
            created_at=datetime.utcnow()
        )
        db.session.add(blacklist_entry)
        db.session.commit()
        
        headers = {
            "Authorization": "Bearer test-token"
        }
        
        response = self.client.get('/blacklists/blacklisted@example.com', 
                                   headers=headers)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data["blacklisted"])
        self.assertEqual(response_data["email"], "blacklisted@example.com")
        self.assertEqual(response_data["blocked_reason"], "Spam detected")

    def test_check_non_blacklisted_email(self):
        """Test checking if a non-blacklisted email"""
        headers = {
            "Authorization": "Bearer test-token"
        }
        
        response = self.client.get('/blacklists/clean@example.com', 
                                   headers=headers)
        
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
        
        response = self.client.post('/blacklists', 
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 401)

    def test_invalid_email_format(self):
        """Test adding invalid email format"""
        data = {
            "email": "invalid-email",
            "app_uuid": "12345678-1234-1234-1234-123456789012",
            "blocked_reason": "Spam detected"
        }
        
        headers = {
            "Authorization": "Bearer test-token",
            "Content-Type": "application/json"
        }
        
        response = self.client.post('/blacklists', 
                                    data=json.dumps(data), 
                                    headers=headers)
        
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()