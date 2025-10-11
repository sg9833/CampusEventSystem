"""
Unit Tests for Configuration Management
Tests settings loading, validation, and access patterns
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from config.settings import Settings, settings, get_settings, reload_settings


class TestSettings:
    """Test suite for Settings class"""
    
    def test_singleton_pattern(self):
        """Test that Settings follows singleton pattern"""
        # Arrange & Act
        settings1 = Settings()
        settings2 = Settings()
        
        # Assert
        assert settings1 is settings2
    
    def test_default_values_loaded(self):
        """Test that default values are loaded"""
        # Arrange & Act
        config = Settings()
        
        # Assert
        assert config.API_BASE_URL is not None
        assert config.API_TIMEOUT == 30
        assert config.CACHE_ENABLED == True
        assert config.LOG_LEVEL == 'INFO'
    
    def test_get_method(self):
        """Test get method with default"""
        # Arrange
        config = Settings()
        
        # Act
        value1 = config.get('API_BASE_URL')
        value2 = config.get('NONEXISTENT_KEY', 'default_value')
        
        # Assert
        assert value1 is not None
        assert value2 == 'default_value'
    
    def test_attribute_access(self):
        """Test attribute-style access"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert hasattr(config, 'API_BASE_URL')
        assert config.API_BASE_URL is not None
    
    def test_dictionary_access(self):
        """Test dictionary-style access"""
        # Arrange
        config = Settings()
        
        # Act
        value = config['API_BASE_URL']
        
        # Assert
        assert value is not None
    
    def test_set_method(self):
        """Test set method for runtime changes"""
        # Arrange
        config = Settings()
        
        # Act
        config.set('CUSTOM_KEY', 'custom_value')
        
        # Assert
        assert config.get('CUSTOM_KEY') == 'custom_value'
    
    def test_is_development(self):
        """Test environment detection - development"""
        # Arrange
        config = Settings(env='development')
        
        # Act & Assert
        assert config.is_development() == True
        assert config.is_production() == False
        assert config.is_testing() == False
    
    def test_is_production(self):
        """Test environment detection - production"""
        # Arrange
        config = Settings(env='production')
        
        # Act & Assert
        assert config.is_development() == False
        assert config.is_production() == True
        assert config.is_testing() == False
    
    def test_to_dict(self):
        """Test exporting config as dictionary"""
        # Arrange
        config = Settings()
        
        # Act
        config_dict = config.to_dict()
        
        # Assert
        assert isinstance(config_dict, dict)
        assert 'API_BASE_URL' in config_dict
        assert len(config_dict) > 0


class TestConfigParsing:
    """Test configuration value parsing"""
    
    def test_parse_boolean_true(self):
        """Test parsing boolean true values"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert config._parse_value('true') == True
        assert config._parse_value('True') == True
        assert config._parse_value('yes') == True
        assert config._parse_value('1') == True
        assert config._parse_value('on') == True
    
    def test_parse_boolean_false(self):
        """Test parsing boolean false values"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert config._parse_value('false') == False
        assert config._parse_value('False') == False
        assert config._parse_value('no') == False
        assert config._parse_value('0') == False
        assert config._parse_value('off') == False
    
    def test_parse_integer(self):
        """Test parsing integer values"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert config._parse_value('42') == 42
        assert config._parse_value('-10') == -10
        assert config._parse_value('0') == 0
    
    def test_parse_float(self):
        """Test parsing float values"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert config._parse_value('3.14') == 3.14
        assert config._parse_value('-2.5') == -2.5
    
    def test_parse_none(self):
        """Test parsing null/none values"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert config._parse_value('none') is None
        assert config._parse_value('null') is None
        assert config._parse_value('') is None
    
    def test_parse_string(self):
        """Test parsing string values"""
        # Arrange
        config = Settings()
        
        # Act & Assert
        assert config._parse_value('hello') == 'hello'
        assert config._parse_value('http://localhost') == 'http://localhost'


class TestConfigValidation:
    """Test configuration validation"""
    
    def test_required_fields_present(self):
        """Test that required fields are validated"""
        # Arrange & Act
        config = Settings()
        
        # Assert - should not raise exception
        assert config.API_BASE_URL is not None
    
    def test_api_url_validation(self):
        """Test API URL format validation"""
        # Arrange
        config = Settings()
        
        # Act
        api_url = config.API_BASE_URL
        
        # Assert
        assert api_url.startswith('http://') or api_url.startswith('https://')


class TestEnvironmentVariables:
    """Test environment variable loading"""
    
    @patch.dict(os.environ, {'API_BASE_URL': 'http://test.com/api'})
    def test_env_var_override(self):
        """Test that environment variables override defaults"""
        # Arrange & Act
        config = Settings()
        config._load_all_config()
        
        # Assert
        assert config.API_BASE_URL == 'http://test.com/api'
    
    @patch.dict(os.environ, {'API_TIMEOUT': '60'})
    def test_env_var_type_conversion(self):
        """Test that env vars are converted to correct types"""
        # Arrange & Act
        config = Settings()
        config._load_all_config()
        
        # Assert
        assert config.API_TIMEOUT == 60
        assert isinstance(config.API_TIMEOUT, int)


class TestGlobalInstance:
    """Test global settings instance"""
    
    def test_global_settings_accessible(self):
        """Test that global settings instance is accessible"""
        # Arrange
        from config.settings import settings
        
        # Act & Assert
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_get_settings_function(self):
        """Test get_settings convenience function"""
        # Arrange & Act
        config = get_settings()
        
        # Assert
        assert config is not None
        assert isinstance(config, Settings)
    
    def test_reload_settings_function(self):
        """Test reload_settings function"""
        # Arrange & Act
        try:
            reload_settings()
            # Assert - should not raise exception
            assert True
        except Exception as e:
            pytest.fail(f"reload_settings raised exception: {e}")


class TestConfigHelpers:
    """Test configuration helper functions"""
    
    def test_get_api_base_url(self):
        """Test get_api_base_url helper"""
        # Arrange
        from config.settings import get_api_base_url
        
        # Act
        url = get_api_base_url()
        
        # Assert
        assert url is not None
        assert isinstance(url, str)
    
    def test_get_cache_dir(self):
        """Test get_cache_dir helper"""
        # Arrange
        from config.settings import get_cache_dir
        
        # Act
        cache_dir = get_cache_dir()
        
        # Assert
        assert cache_dir is not None
        assert isinstance(cache_dir, str)
    
    def test_get_log_dir(self):
        """Test get_log_dir helper"""
        # Arrange
        from config.settings import get_log_dir
        
        # Act
        log_dir = get_log_dir()
        
        # Assert
        assert log_dir is not None
        assert isinstance(log_dir, str)
