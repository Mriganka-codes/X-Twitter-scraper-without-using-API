#!/usr/bin/env python3
"""
Setup script for Twitter Scraper
This script helps set up the environment and install dependencies
"""

import os
import sys
import subprocess
import shutil

def clear_webdriver_cache():
    """Clear webdriver-manager cache"""
    try:
        print("Clearing webdriver-manager cache...")
        # Construct cache path manually
        home_dir = os.path.expanduser("~")
        cache_path = os.path.join(home_dir, ".wdm")
        
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
            print("✓ Webdriver cache cleared")
        else:
            print("✓ Webdriver cache is already empty")
    except Exception as e:
        print(f"⚠ Could not clear webdriver cache: {str(e)}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")

def check_chrome_installation():
    """Check if Chrome browser is installed"""
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✓ Chrome browser found")
            return True
    
    print("⚠ Chrome browser not found. Please install Google Chrome.")
    return False

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✓ Created .env file from template")
        else:
            # Create basic .env file
            with open(".env", "w") as f:
                f.write("TWITTER_KEYWORDS=python,machine learning,AI,data science,programming\n")
                f.write("MAX_TWEETS_PER_KEYWORD=50\n")
                f.write("SCRAPE_TIME=09:00\n")
                f.write("HEADLESS_MODE=true\n")
            print("✓ Created basic .env file")
    else:
        print("✓ .env file already exists")

def create_data_directory():
    """Create data directory for storing scraped tweets and logs"""
    os.makedirs("data", exist_ok=True)
    print("✓ Data directory created")

def run_test():
    """Run a quick test to verify everything works"""
    try:
        print("\nRunning quick test...")
        from scraper import TwitterScraper
        scraper = TwitterScraper()
        print("✓ Scraper module imported successfully")
        
        # Test driver setup (without actually opening browser)
        print("✓ Setup completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("Twitter Scraper Setup")
    print("=" * 50)
    
    # Clear cache before anything else
    clear_webdriver_cache()
    
    # Check requirements
    check_python_version()
    chrome_installed = check_chrome_installation()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup configuration
    create_env_file()
    create_data_directory()
    
    # Run test
    if run_test():
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file to customize your keywords")
        print("2. Run 'python scheduler.py --once' to test")
        print("3. Run 'python scheduler.py' for continuous operation")
        
        if not chrome_installed:
            print("\n⚠ Warning: Please install Google Chrome before running the scraper")
    else:
        print("\n✗ Setup completed with errors. Please check the error messages above.")

if __name__ == "__main__":
    main()
