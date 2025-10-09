import unittest
from unittest.mock import Mock
from src.application.health_service import HealthService


class TestHealthService(unittest.TestCase):
    """Test cases for HealthService"""

    def setUp(self):
        self.mock_health_check = Mock()
        self.health_service = HealthService(self.mock_health_check)

    def test_get_health_status_healthy(self):
        """Test health status when all systems are healthy"""
        # Arrange
        self.mock_health_check.check_database_health.return_value = True
        self.mock_health_check.check_external_services_health.return_value = True

        # Act
        result = self.health_service.get_health_status()

        # Assert
        self.assertEqual(result.status, "healthy")
        self.assertEqual(result.message, "All systems operational")

    def test_get_health_status_unhealthy(self):
        """Test health status when some systems are down"""
        # Arrange
        self.mock_health_check.check_database_health.return_value = False
        self.mock_health_check.check_external_services_health.return_value = True

        # Act
        result = self.health_service.get_health_status()

        # Assert
        self.assertEqual(result.status, "unhealthy")
        self.assertEqual(result.message, "Some systems are down")

    def test_get_health_status_error(self):
        """Test health status when an error occurs"""
        # Arrange
        self.mock_health_check.check_database_health.side_effect = Exception("Database error")

        # Act
        result = self.health_service.get_health_status()

        # Assert
        self.assertEqual(result.status, "error")
        self.assertIn("Health check failed", result.message)

    def test_ping(self):
        """Test ping endpoint"""
        # Act
        result = self.health_service.ping()

        # Assert
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["message"], "pong")
        self.assertIn("timestamp", result)


if __name__ == "__main__":
    unittest.main()
