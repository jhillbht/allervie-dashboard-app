# Root app.py file to help buildpack detection
# This just imports and runs the actual app from the backend directory

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the app from the backend directory
from backend.app import app

if __name__ == "__main__":
    # Get port from environment variable or use 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)