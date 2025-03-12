#!/bin/bash
# Deploy the Allervie Analytics Dashboard to DigitalOcean App Platform

set -e  # Exit on any error

# Configuration
APP_NAME="allervie-analytics-dashboard"
GITHUB_REPO="yourusername/allervie-dashboard-app"
BRANCH="main"
DEPLOYMENT_ENV=${1:-"production"}  # Default to production unless specified

echo "=== Deploying Allervie Analytics Dashboard to DigitalOcean ==="
echo "Environment: $DEPLOYMENT_ENV"

# Check for doctl CLI tool
if ! command -v doctl &> /dev/null; then
    echo "Error: doctl CLI not installed. Please install it first."
    echo "See: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check for authenticated doctl
if ! doctl account get &> /dev/null; then
    echo "Error: doctl not authenticated. Please run 'doctl auth init' first."
    exit 1
fi

# Check if google-ads.yaml exists for encoding
if [ ! -f "./backend/google-ads.yaml" ]; then
    echo "Error: google-ads.yaml not found in ./backend directory"
    echo "Please create this file with your Google Ads API credentials"
    exit 1
fi

# Encode google-ads.yaml to base64 for secrets
GOOGLE_ADS_YAML_B64=$(base64 -i ./backend/google-ads.yaml)

echo "=== Creating/updating app configuration ==="

# Create app.yaml dynamically
cat > app.yaml << EOL
name: $APP_NAME
services:
- name: api
  github:
    branch: $BRANCH
    deploy_on_push: true
    repo: $GITHUB_REPO
  envs:
  - key: FLASK_APP
    value: backend/app.py
  - key: FLASK_ENV
    value: $DEPLOYMENT_ENV
  - key: ALLOW_MOCK_DATA
    value: "false"
  - key: APP_URL
    scope: RUN_AND_BUILD_TIME
    value: \${APP_URL}
  - key: AUTO_REFRESH_TOKENS
    value: "true"
  - key: ENVIRONMENT
    value: $DEPLOYMENT_ENV
  - key: USE_REAL_ADS_CLIENT
    value: "true"
  - key: GOOGLE_ADS_YAML
    scope: RUN_TIME
    type: SECRET
    value: $GOOGLE_ADS_YAML_B64
  run_command: cd backend && gunicorn app:app
  instance_size_slug: basic-xxs
  routes:
  - path: /
  source_dir: /
EOL

echo "=== Checking if app exists ==="
if doctl apps list --format Name | grep -q "^$APP_NAME$"; then
    echo "App exists, updating..."
    doctl apps update "$APP_NAME" --spec app.yaml
else
    echo "App doesn't exist, creating..."
    doctl apps create --spec app.yaml
fi

echo "=== Deployment initiated ==="
echo "Check deployment status with: doctl apps get $APP_NAME"
echo "Note: The first deployment may take a few minutes to complete."
echo "Access your dashboard at the URL provided in the DigitalOcean App Platform console."

# Cleanup
echo "=== Cleaning up temporary files ==="
rm app.yaml

echo "=== Deployment process completed ==="