"""
API testing client
"""
import requests
import json
from typing import Dict, Any, Optional
from loguru import logger
from framework.utils.config_loader import ConfigLoader


class APIClient:
    """Client for API testing"""
    
    def __init__(self, base_url: str = None):
        self.config = ConfigLoader().load_config()
        self.base_url = base_url or self.config['app']['api']['base_url']
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session.headers.update(self.headers)
    
    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        logger.info("Authentication token set")
    
    def get(self, endpoint: str, params: Dict = None, **kwargs) -> requests.Response:
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params, **kwargs)
        logger.info(f"Response status: {response.status_code}")
        return response
    
    def post(self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs) -> requests.Response:
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        if json_data:
            response = self.session.post(url, json=json_data, **kwargs)
        else:
            response = self.session.post(url, data=data, **kwargs)
        logger.info(f"Response status: {response.status_code}")
        return response
    
    def put(self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs) -> requests.Response:
        """Make PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        if json_data:
            response = self.session.put(url, json=json_data, **kwargs)
        else:
            response = self.session.put(url, data=data, **kwargs)
        logger.info(f"Response status: {response.status_code}")
        return response
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, **kwargs)
        logger.info(f"Response status: {response.status_code}")
        return response
    
    def validate_response(self, response: requests.Response, 
                         expected_status: int = 200,
                         schema: Dict = None) -> Dict[str, Any]:
        """Validate API response"""
        results = {
            'status_code_match': response.status_code == expected_status,
            'is_json': False,
            'data': None,
            'errors': []
        }
        
        # Check status code
        if not results['status_code_match']:
            results['errors'].append(
                f"Expected status {expected_status}, got {response.status_code}"
            )
        
        # Check if JSON
        try:
            results['data'] = response.json()
            results['is_json'] = True
        except:
            results['errors'].append("Response is not valid JSON")
        
        # Validate schema if provided
        if schema and results['is_json']:
            # Schema validation would go here (using jsonschema)
            pass
        
        results['valid'] = len(results['errors']) == 0
        return results
