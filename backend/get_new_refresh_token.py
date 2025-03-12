#!/usr/bin/env python3
"""Script to generate a new Google Ads API refresh token."""

import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import requests
import yaml

# Load the google-ads.yaml file to get client ID and client secret
def load_yaml():
    """Load the google-ads.yaml file."""
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google-ads.yaml")
    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found")
        sys.exit(1)
    
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)
    return config

# OAuth server to capture the authorization code
class OAuthHandler(BaseHTTPRequestHandler):
    """HTTP request handler to capture OAuth authorization code."""
    
    def do_GET(self):
        """Handle GET request with authorization code."""
        query = parse_qs(urlparse(self.path).query)
        
        if "code" in query:
            self.server.authorization_code = query["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head><title>OAuth Success</title></head>")
            self.wfile.write(b"<body><h1>Authorization Successful!</h1>")
            self.wfile.write(b"<p>You can now close this window and return to the terminal.</p>")
            self.wfile.write(b"</body></html>")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head><title>OAuth Error</title></head>")
            self.wfile.write(b"<body><h1>Authorization Failed</h1>")
            self.wfile.write(b"<p>No authorization code received.</p>")
            self.wfile.write(b"</body></html>")

def get_authorization_code(client_id):
    """Get authorization code from OAuth flow."""
    redirect_uri = "http://localhost:8080"
    scope = "https://www.googleapis.com/auth/adwords"
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        "&response_type=code"
        "&access_type=offline"
        "&prompt=consent"
    )
    
    print(f"Opening browser window for authorization...")
    webbrowser.open(auth_url)
    
    # Start a simple HTTP server to capture the authorization code
    server = HTTPServer(("localhost", 8080), OAuthHandler)
    server.authorization_code = None
    
    print("Waiting for authorization...")
    while server.authorization_code is None:
        server.handle_request()
    
    return server.authorization_code

def exchange_code_for_tokens(client_id, client_secret, authorization_code):
    """Exchange authorization code for refresh token."""
    token_url = "https://oauth2.googleapis.com/token"
    redirect_uri = "http://localhost:8080"
    
    token_data = {
        "code": authorization_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(token_url, data=token_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error exchanging code for tokens: {response.text}")
        sys.exit(1)

def update_yaml(refresh_token):
    """Update the google-ads.yaml file with the new refresh token."""
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google-ads.yaml")
    
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)
    
    config["refresh_token"] = refresh_token
    
    with open(yaml_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False)

def main():
    """Main function to generate refresh token."""
    print("=== Google Ads API Refresh Token Generator ===")
    
    config = load_yaml()
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")
    
    if not client_id or not client_secret:
        print("Error: client_id or client_secret not found in google-ads.yaml")
        sys.exit(1)
    
    print(f"Using client ID: {client_id}")
    auth_code = get_authorization_code(client_id)
    
    print("Authorization code received, exchanging for tokens...")
    tokens = exchange_code_for_tokens(client_id, client_secret, auth_code)
    
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        print("Error: No refresh token received")
        sys.exit(1)
    
    print(f"Refresh token obtained: {refresh_token}")
    update_yaml(refresh_token)
    
    print("=== Success ===")
    print("Refresh token has been updated in google-ads.yaml")
    print("You're now ready to use the Google Ads API!")

if __name__ == "__main__":
    main()
