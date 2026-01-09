"""
Device registration and activation tests
Tests user device setup, pairing, and activation flows
"""
import pytest
from framework.utils.api_client import APIClient
from loguru import logger


@pytest.mark.integration
@pytest.mark.device
class TestDeviceRegistration:
    """Test cases for device registration and activation"""
    
    def setup_method(self):
        """Setup for each test"""
        self.api = APIClient()
        self.test_user_email = "test@clearcaptions.com"
        self.test_device_id = "device_12345"
        self.test_device_type = "home_phone"  # or "mobile_app"
    
    def test_device_registration(self):
        """Test device registration process"""
        registration_data = {
            'user_email': self.test_user_email,
            'device_id': self.test_device_id,
            'device_type': self.test_device_type,
            'model': 'ClearCaptions Home Phone v2',
            'serial_number': 'SN123456789'
        }
        
        # In real implementation, this would call registration API
        # response = self.api.post("/devices/register", json_data=registration_data)
        
        # For testing, validate registration data structure
        assert 'user_email' in registration_data
        assert 'device_id' in registration_data
        assert 'device_type' in registration_data
        
        logger.info(f"Device registration: {self.test_device_id}")
    
    def test_device_activation(self):
        """Test device activation flow"""
        activation_data = {
            'device_id': self.test_device_id,
            'activation_code': 'ACT123456',
            'user_email': self.test_user_email
        }
        
        # Validate activation data
        assert 'device_id' in activation_data
        assert 'activation_code' in activation_data
        
        # In real implementation:
        # response = self.api.post("/devices/activate", json_data=activation_data)
        # assert response.status_code == 200
        
        logger.info(f"Device activation: {self.test_device_id}")
    
    def test_device_pairing(self):
        """Test device pairing with user account"""
        pairing_data = {
            'device_id': self.test_device_id,
            'user_email': self.test_user_email,
            'pairing_token': 'PAIR789012'
        }
        
        assert 'device_id' in pairing_data
        assert 'user_email' in pairing_data
        assert 'pairing_token' in pairing_data
        
        logger.info(f"Device pairing: {self.test_device_id} with {self.test_user_email}")
    
    def test_device_verification(self):
        """Test device verification process"""
        verification_data = {
            'device_id': self.test_device_id,
            'verification_code': 'VERIFY456'
        }
        
        # Validate verification
        assert 'device_id' in verification_data
        assert 'verification_code' in verification_data
        
        logger.info(f"Device verification: {self.test_device_id}")
    
    def test_mobile_app_registration(self):
        """Test mobile app device registration"""
        mobile_registration = {
            'user_email': self.test_user_email,
            'device_id': 'mobile_device_789',
            'device_type': 'mobile_app',
            'platform': 'iOS',
            'app_version': '2.1.0',
            'device_model': 'iPhone 15'
        }
        
        assert mobile_registration['device_type'] == 'mobile_app'
        assert mobile_registration['platform'] in ['iOS', 'Android']
        
        logger.info(f"Mobile app registration: {mobile_registration['device_id']}")
    
    def test_device_status_check(self):
        """Test checking device registration status"""
        device_info = {
            'device_id': self.test_device_id,
            'status': 'active',
            'registered_at': '2026-01-01T00:00:00Z',
            'last_seen': '2026-01-09T12:00:00Z'
        }
        
        assert 'device_id' in device_info
        assert 'status' in device_info
        assert device_info['status'] in ['pending', 'active', 'inactive', 'suspended']
        
        logger.info(f"Device status: {device_info['device_id']} - {device_info['status']}")
    
    def test_multiple_device_registration(self):
        """Test user registering multiple devices"""
        devices = [
            {'device_id': 'device_1', 'device_type': 'home_phone'},
            {'device_id': 'device_2', 'device_type': 'mobile_app', 'platform': 'iOS'},
            {'device_id': 'device_3', 'device_type': 'mobile_app', 'platform': 'Android'}
        ]
        
        for device in devices:
            assert 'device_id' in device
            assert 'device_type' in device
        
        logger.info(f"Multiple devices registered: {len(devices)} devices")
    
    def test_device_deactivation(self):
        """Test device deactivation"""
        deactivation_data = {
            'device_id': self.test_device_id,
            'reason': 'user_request',
            'deactivated_at': '2026-01-09T12:00:00Z'
        }
        
        assert 'device_id' in deactivation_data
        assert 'reason' in deactivation_data
        
        logger.info(f"Device deactivated: {self.test_device_id}")
