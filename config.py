import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    
     # --- NEW: Add credentials from .env file ---
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
    # --- END NEW ---


    # Keywords to search for (can be modified in .env file)
    KEYWORDS = [
        "python",
        "machine learning",
        "AI",
        "data science",
        "programming"
    ]
    
    # Scraping settings
    MAX_TWEETS_PER_KEYWORD = 100
    SCROLL_PAUSE_TIME = 2
    IMPLICIT_WAIT_TIME = 10
    
    # File paths
    DATA_DIR = "data"
    TWEETS_FILE = os.path.join(DATA_DIR, "scraped_tweets.csv")
    LOG_FILE = os.path.join(DATA_DIR, "scraper.log")
    
    # Browser settings
    HEADLESS_MODE = True
    BROWSER_TIMEOUT = 60
    
    # Scheduling
    SCRAPE_TIME = "09:00"  # 24-hour format
    
    # Twitter URLs
    TWITTER_SEARCH_URL = "https://twitter.com/search?q={}&src=typed_query&f=live"
    
    @classmethod
    def get_keywords_from_env(cls):
        """Get keywords from environment variable if set"""
        env_keywords = os.getenv('TWITTER_KEYWORDS')
        if env_keywords:
            return [keyword.strip() for keyword in env_keywords.split(',')]
        return cls.KEYWORDS
