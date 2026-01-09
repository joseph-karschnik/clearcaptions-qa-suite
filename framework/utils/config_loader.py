"""
Configuration loader utility
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages configuration files"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Default to config directory
            base_path = Path(__file__).parent.parent.parent
            config_path = base_path / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
        self._config = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if self._config is None:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            
            # Load environment-specific config
            env = self._config.get('environment', 'staging')
            env_config_path = self.config_path.parent / "environments.yaml"
            
            if env_config_path.exists():
                with open(env_config_path, 'r') as f:
                    env_configs = yaml.safe_load(f)
                    if env in env_configs:
                        # Merge environment config
                        self._merge_config(self._config, env_configs[env])
            
            # Replace environment variables
            self._replace_env_vars(self._config)
        
        return self._config
    
    def _merge_config(self, base: Dict, override: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _replace_env_vars(self, config: Dict):
        """Replace ${VAR} placeholders with environment variables"""
        if isinstance(config, dict):
            for key, value in config.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    config[key] = os.getenv(env_var, value)
                elif isinstance(value, dict):
                    self._replace_env_vars(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._replace_env_vars(item)
        elif isinstance(config, list):
            for item in config:
                if isinstance(item, dict):
                    self._replace_env_vars(item)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        config = self.load_config()
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
