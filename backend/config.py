# Global configuration variables
import os

# Environment variables with fallbacks
def get_env_var(var_name, default_value):
    """Get environment variable with fallback default value."""
    return os.environ.get(var_name, default_value)

# Set to True to always attempt to use real Google Ads data
# instead of mock data, even with mock authentication tokens
USE_REAL_ADS_CLIENT = get_env_var("USE_REAL_ADS_CLIENT", "True").lower() == "true"

# Set to False to force real data only (no mock data fallback)
ALLOW_MOCK_DATA = get_env_var("ALLOW_MOCK_DATA", "False").lower() == "true"

# Set to False to disable mock authentication
ALLOW_MOCK_AUTH = get_env_var("ALLOW_MOCK_AUTH", "False").lower() == "true"

# Set environment (development or production)
ENVIRONMENT = get_env_var("ENVIRONMENT", "production")

# This is the customer ID to use for Google Ads API requests
CLIENT_CUSTOMER_ID = get_env_var("CLIENT_CUSTOMER_ID", "")

# Token refresh settings
TOKEN_AUTO_REFRESH_ENABLED = get_env_var("TOKEN_AUTO_REFRESH_ENABLED", "True").lower() == "true"
AUTO_REFRESH_INTERVAL_MINUTES = int(get_env_var("AUTO_REFRESH_INTERVAL_MINUTES", "30"))
USE_ENHANCED_REFRESH = get_env_var("USE_ENHANCED_REFRESH", "True").lower() == "true"

# The base URL of the application, used for OAuth redirects
APP_URL = get_env_var("APP_URL", "localhost:5002")

# Google Ads API version
GOOGLE_ADS_API_VERSION = get_env_var("GOOGLE_ADS_API_VERSION", "v17")