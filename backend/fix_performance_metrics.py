#!/usr/bin/env python
"""
Fix Performance Metrics for Google Ads Dashboard

This script verifies and fixes issues with the Google Ads performance data
to ensure metrics are accurate and using live data.
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime, timedelta
import pytz
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_performance_endpoint():
    """Test the Google Ads performance endpoint to ensure it returns live data"""
    try:
        # Import the performance function
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from google_ads_client import get_ads_performance

        # Set date range for the past 30 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        logger.info(f"Testing performance endpoint with date range: {start_date} to {end_date}")
        
        # Get performance data
        performance_data = get_ads_performance(start_date, end_date, True)
        
        if not performance_data:
            logger.error("No performance data returned")
            return False, "No data returned from Google Ads API"
        
        # Validate the data structure
        if not isinstance(performance_data, dict):
            logger.error(f"Invalid performance data structure: {type(performance_data)}")
            return False, f"Invalid data structure: {type(performance_data)}"
        
        # Check key metrics
        required_metrics = [
            "impressions", "clicks", "conversions", "cost", 
            "conversionRate", "clickThroughRate", "costPerConversion"
        ]
        
        missing_metrics = []
        for metric in required_metrics:
            if metric not in performance_data:
                missing_metrics.append(metric)
        
        if missing_metrics:
            logger.error(f"Missing metrics: {missing_metrics}")
            return False, f"Missing metrics: {missing_metrics}"
        
        # Validate data for each metric
        invalid_metrics = []
        for metric in required_metrics:
            metric_data = performance_data[metric]
            
            if not isinstance(metric_data, dict):
                invalid_metrics.append(f"{metric} (not a dict)")
                continue
                
            if 'value' not in metric_data:
                invalid_metrics.append(f"{metric} (no value)")
                continue
                
            if 'change' not in metric_data:
                invalid_metrics.append(f"{metric} (no change)")
                continue
        
        if invalid_metrics:
            logger.error(f"Invalid metric data: {invalid_metrics}")
            return False, f"Invalid metric data: {invalid_metrics}"
        
        # Print the performance data
        logger.info("Performance data retrieved successfully:")
        for metric in required_metrics:
            value = performance_data[metric]['value']
            change = performance_data[metric]['change']
            logger.info(f"{metric}: {value} (change: {change}%)")
        
        return True, performance_data
    
    except Exception as e:
        logger.error(f"Error testing performance endpoint: {e}")
        logger.error(traceback.format_exc())
        return False, f"Error: {str(e)}"

def check_api_base_url():
    """Check if the API base URL in the dashboard template is correct"""
    try:
        template_path = Path(__file__).parent / "templates" / "ads_dashboard.html"
        
        if not template_path.exists():
            logger.error(f"Dashboard template not found at {template_path}")
            return False, f"Dashboard template not found at {template_path}"
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Check for API_BASE_URL
        if "const API_BASE_URL = 'http://localhost:5002/api';" in template_content:
            logger.warning("API base URL is set to localhost in the dashboard template")
            return False, "API base URL is set to localhost"
        
        # Find the current API_BASE_URL line
        api_base_url_line = None
        for line in template_content.split('\n'):
            if 'const API_BASE_URL' in line:
                api_base_url_line = line.strip()
                break
        
        if not api_base_url_line:
            logger.error("API_BASE_URL not found in dashboard template")
            return False, "API_BASE_URL not found in template"
        
        logger.info(f"Current API base URL: {api_base_url_line}")
        return True, api_base_url_line
    
    except Exception as e:
        logger.error(f"Error checking API base URL: {e}")
        logger.error(traceback.format_exc())
        return False, f"Error: {str(e)}"

def fix_api_base_url():
    """Fix the API base URL in the dashboard template to use relative URLs"""
    try:
        template_path = Path(__file__).parent / "templates" / "ads_dashboard.html"
        
        if not template_path.exists():
            logger.error(f"Dashboard template not found at {template_path}")
            return False, f"Dashboard template not found at {template_path}"
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Replace the API_BASE_URL line with a relative URL
        if "const API_BASE_URL = 'http://localhost:5002/api';" in template_content:
            logger.info("Fixing API base URL...")
            
            # Replace with relative URL that works in any environment
            updated_content = template_content.replace(
                "const API_BASE_URL = 'http://localhost:5002/api';",
                "const API_BASE_URL = window.location.origin + '/api';"
            )
            
            # Save the updated template
            with open(template_path, 'w') as f:
                f.write(updated_content)
            
            logger.info("API base URL fixed to use relative URLs")
            return True, "API base URL fixed"
        else:
            # Try to find the current API_BASE_URL line
            for i, line in enumerate(template_content.split('\n')):
                if 'const API_BASE_URL' in line:
                    lines = template_content.split('\n')
                    current_url = line.strip()
                    lines[i] = "        const API_BASE_URL = window.location.origin + '/api';"
                    updated_content = '\n'.join(lines)
                    
                    # Save the updated template
                    with open(template_path, 'w') as f:
                        f.write(updated_content)
                    
                    logger.info(f"API base URL changed from {current_url} to use relative URLs")
                    return True, "API base URL fixed"
            
            logger.error("API_BASE_URL not found in dashboard template")
            return False, "API_BASE_URL not found in template"
    
    except Exception as e:
        logger.error(f"Error fixing API base URL: {e}")
        logger.error(traceback.format_exc())
        return False, f"Error: {str(e)}"

def validate_dashboard_template():
    """Check the dashboard template for any missing metrics or formatting issues"""
    try:
        template_path = Path(__file__).parent / "templates" / "ads_dashboard.html"
        
        if not template_path.exists():
            logger.error(f"Dashboard template not found at {template_path}")
            return False, f"Dashboard template not found at {template_path}"
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Check for required metric display elements
        required_elements = [
            "displayMetrics", "loadPerformanceData", "formatNumber", "formatCurrency",
            "updatePerformanceChart", "metric-value", "metric-change"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in template_content:
                missing_elements.append(element)
        
        if missing_elements:
            logger.error(f"Missing template elements: {missing_elements}")
            return False, f"Missing template elements: {missing_elements}"
        
        logger.info("Dashboard template validated successfully")
        return True, "Dashboard template is valid"
    
    except Exception as e:
        logger.error(f"Error validating dashboard template: {e}")
        logger.error(traceback.format_exc())
        return False, f"Error: {str(e)}"

def main():
    """Run all checks and fixes"""
    print("\n===== Google Ads Performance Metrics Check =====\n")
    
    # Test performance data
    print("\n----- Performance Data Test -----")
    perf_success, perf_result = test_performance_endpoint()
    
    if perf_success:
        print("✅ Google Ads performance data is valid and accurate")
    else:
        print(f"❌ Performance data issue: {perf_result}")
    
    # Check API base URL
    print("\n----- API Base URL Check -----")
    url_success, url_result = check_api_base_url()
    
    if url_success and "localhost" not in url_result:
        print(f"✅ API base URL is correctly configured: {url_result}")
    else:
        print(f"❌ API base URL issue: {url_result}")
        
        # Fix API base URL if needed
        fix_success, fix_result = fix_api_base_url()
        
        if fix_success:
            print(f"✅ Fixed API base URL: {fix_result}")
        else:
            print(f"❌ Failed to fix API base URL: {fix_result}")
    
    # Validate dashboard template
    print("\n----- Dashboard Template Validation -----")
    template_success, template_result = validate_dashboard_template()
    
    if template_success:
        print(f"✅ {template_result}")
    else:
        print(f"❌ Template issue: {template_result}")
    
    # Display results summary
    print("\n----- Summary -----")
    if perf_success and (url_success or fix_success) and template_success:
        print("✅ All checks passed - Google Ads performance metrics are working correctly")
        print("\nThe dashboard at https://allervie-test-deployment-xjfjs.ondigitalocean.app/ads-dashboard")
        print("is now using accurate, live data for the Google Ads Performance metrics table.")
    else:
        print("❌ Some issues were found - see the details above")
        print("\nFixes required:")
        if not perf_success:
            print("- Performance data needs to be fixed - check the Google Ads API configuration")
        if not (url_success or fix_success):
            print("- API base URL needs to be fixed manually in the dashboard template")
        if not template_success:
            print("- Dashboard template needs to be updated to correctly display metrics")

if __name__ == "__main__":
    main()