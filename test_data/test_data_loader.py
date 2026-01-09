"""
Test data loader utility
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger


class TestDataLoader:
    """Loads test data from YAML files"""
    
    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = Path(data_dir)
    
    def load_users(self) -> Dict[str, Any]:
        """Load test user data"""
        filepath = self.data_dir / "test_users.yaml"
        
        if not filepath.exists():
            logger.warning(f"Test users file not found: {filepath}")
            return {}
        
        with open(filepath, 'r') as f:
            content = f.read()
            # Replace environment variables
            for key, value in os.environ.items():
                content = content.replace(f"${{{key}}}", value)
            data = yaml.safe_load(content)
        
        return data.get('test_users', {})
    
    def load_caption_test_cases(self) -> List[Dict[str, Any]]:
        """Load caption quality test cases"""
        filepath = self.data_dir / "caption_test_cases.yaml"
        
        if not filepath.exists():
            logger.warning(f"Caption test cases file not found: {filepath}")
            return []
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        test_cases = []
        for case_name, case_data in data.get('caption_test_cases', {}).items():
            test_cases.append({
                'name': case_name,
                'reference': case_data.get('reference', ''),
                'expected_wer': case_data.get('expected_wer', 0.05),
                'category': case_data.get('category', 'general')
            })
        
        return test_cases
    
    def get_user(self, user_type: str = "standard_user") -> Dict[str, Any]:
        """Get specific test user"""
        users = self.load_users()
        return users.get(user_type, {})
    
    def get_invalid_user(self, user_type: str = "invalid_email") -> Dict[str, Any]:
        """Get invalid test user"""
        filepath = self.data_dir / "test_users.yaml"
        
        if not filepath.exists():
            return {}
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        return data.get('invalid_users', {}).get(user_type, {})
