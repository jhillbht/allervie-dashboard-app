# Allervie Analytics Dashboard

A comprehensive Google Ads API analytics dashboard with enhanced OAuth integration, automatic token refresh, and optimized data presentation.

## Features

- **Enhanced OAuth Integration**: Secure Google OAuth implementation with auto refresh
- **Real-time Google Ads Data**: Campaign, ad group, keyword, and search term performance
- **Responsive Dashboard**: Interactive charts, tables, and performance metrics
- **Multi-environment Support**: Works in development, staging, and production
- **Robust Error Handling**: Graceful fallbacks with detailed error reporting
- **Deployment Ready**: Configuration for DigitalOcean App Platform

## Setup Instructions

### Prerequisites

- Python 3.8+ with pip
- Google Ads API developer token
- Google Cloud OAuth 2.0 client credentials
- Google Ads API access

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/allervie-dashboard-app.git
   cd allervie-dashboard-app
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```

3. Configure Google Ads API:
   ```bash
   cp backend/google-ads.yaml.example backend/google-ads.yaml
   # Edit google-ads.yaml with your credentials
   ```

4. Generate OAuth tokens:
   ```bash
   python backend/get_new_refresh_token.py
   # Follow the prompts to authenticate with Google
   ```

5. Start the development server:
   ```bash
   cd backend
   python app.py
   ```

6. Access the dashboard at http://localhost:5002/ads-dashboard

### Deployment

Use the deployment configuration in `app.yaml` for DigitalOcean App Platform:

1. Create a new DigitalOcean App Platform application
2. Connect your GitHub repository
3. Use the app.yaml configuration
4. Add your Google Ads YAML content as a secret
5. Deploy the application

## Testing

Run the diagnostic tools to verify functionality:

```bash
python backend/check_deployment.py  # Verify deployment configuration
python backend/fix_dashboard_data.py  # Check data quality
python backend/test_ads_connection.py  # Test Google Ads API connection
```

## License

[MIT License](LICENSE)

## Acknowledgments

- Google Ads API
- Flask Framework
- Chart.js for data visualization
- Bootstrap for responsive UI