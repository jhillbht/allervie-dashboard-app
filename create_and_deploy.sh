#!/bin/bash
# Create and deploy the Allervie Analytics Dashboard to DigitalOcean App Platform

set -e  # Exit on any error

echo "=== Allervie Analytics Dashboard Creation and Deployment ==="

# Step 1: Create GitHub repository
echo "=== Step 1: Creating GitHub repository ==="
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Create a public repository? [y/n]: " CREATE_REPO_RESPONSE

if [[ $CREATE_REPO_RESPONSE =~ ^[Yy]$ ]]; then
    echo "Creating GitHub repository..."
    
    if ! command -v gh &> /dev/null; then
        echo "Error: GitHub CLI not installed. Please install it first."
        echo "See: https://cli.github.com/manual/installation"
        exit 1
    fi
    
    # Create GitHub repository
    gh repo create allervie-dashboard-app --public --description "Enhanced Google Ads Analytics Dashboard with OAuth integration" --confirm
    
    # Update remote URL
    git remote add origin "https://github.com/$GITHUB_USERNAME/allervie-dashboard-app.git"
    
    echo "GitHub repository created!"
else
    echo "Skipping GitHub repository creation."
    echo "Please ensure you have a GitHub repository available at:"
    echo "https://github.com/$GITHUB_USERNAME/allervie-dashboard-app"
    
    # Add remote manually
    git remote add origin "https://github.com/$GITHUB_USERNAME/allervie-dashboard-app.git"
fi

# Step 2: Update configuration
echo "=== Step 2: Updating configuration ==="
sed -i '' "s/YOUR_USERNAME/$GITHUB_USERNAME/g" deploy-dashboard.sh
sed -i '' "s/YOUR_USERNAME/$GITHUB_USERNAME/g" app.yaml

echo "Configuration updated with GitHub username: $GITHUB_USERNAME"

# Step 3: Set up Google Ads API credentials
echo "=== Step 3: Setting up Google Ads API credentials ==="
read -p "Set up Google Ads API credentials now? [y/n]: " SETUP_CREDENTIALS_RESPONSE

if [[ $SETUP_CREDENTIALS_RESPONSE =~ ^[Yy]$ ]]; then
    cd backend
    ./setup_google_ads.sh
    cd ..
    echo "Google Ads API credentials set up!"
else
    echo "Skipping Google Ads API credential setup."
    echo "Please set up your credentials before deployment:"
    echo "cd backend && ./setup_google_ads.sh"
fi

# Step 4: Push to GitHub
echo "=== Step 4: Pushing to GitHub ==="
read -p "Push to GitHub now? [y/n]: " PUSH_RESPONSE

if [[ $PUSH_RESPONSE =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "Update configuration with deployment settings"
    git push -u origin main
    echo "Code pushed to GitHub!"
else
    echo "Skipping GitHub push."
    echo "Please push your code manually when ready:"
    echo "git push -u origin main"
fi

# Step 5: Deploy to DigitalOcean
echo "=== Step 5: Deploying to DigitalOcean ==="
read -p "Deploy to DigitalOcean now? [y/n]: " DEPLOY_RESPONSE

if [[ $DEPLOY_RESPONSE =~ ^[Yy]$ ]]; then
    # Check if google-ads.yaml exists before deploying
    if [ ! -f "./backend/google-ads.yaml" ]; then
        echo "Warning: google-ads.yaml not found. Deployment may fail."
        read -p "Continue anyway? [y/n]: " CONTINUE_RESPONSE
        if [[ ! $CONTINUE_RESPONSE =~ ^[Yy]$ ]]; then
            echo "Deployment aborted. Please set up your Google Ads API credentials first."
            exit 1
        fi
    fi
    
    # Deploy with script
    ./deploy-dashboard.sh
    echo "Deployment initiated!"
else
    echo "Skipping DigitalOcean deployment."
    echo "Please deploy manually when ready:"
    echo "./deploy-dashboard.sh"
fi

echo "=== All steps completed! ==="
echo "Your Allervie Analytics Dashboard is ready to use."
echo "Access your dashboard at the URL provided in the DigitalOcean App Platform console."