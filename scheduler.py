import schedule
import time
import logging
from datetime import datetime
from scraper import TwitterScraper
from config import Config

class TwitterScraperScheduler:
    def __init__(self):
        self.setup_logging()
        self.scraper = TwitterScraper()
        
    def setup_logging(self):
        """Setup logging for scheduler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run_scheduled_scraping(self):
        """Run the scraping job"""
        self.logger.info("Starting scheduled Twitter scraping job")
        try:
            self.scraper.run_scraping_session()
            self.logger.info("Scheduled scraping job completed successfully")
        except Exception as e:
            self.logger.error(f"Error in scheduled scraping job: {str(e)}")
            
    def start_scheduler(self):
        """Start the scheduler to run scraping every 24 hours"""
        self.logger.info(f"Starting Twitter scraper scheduler - will run daily at {Config.SCRAPE_TIME}")
        
        # Schedule the job to run daily at specified time
        schedule.every().day.at(Config.SCRAPE_TIME).do(self.run_scheduled_scraping)
        
        # Run once immediately on startup (optional)
        self.logger.info("Running initial scraping session...")
        self.run_scheduled_scraping()
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    def run_once(self):
        """Run scraping once (for testing purposes)"""
        self.logger.info("Running one-time scraping session")
        self.run_scheduled_scraping()

if __name__ == "__main__":
    import sys
    
    scheduler = TwitterScraperScheduler()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run once for testing
        scheduler.run_once()
    else:
        # Start the scheduler
        scheduler.start_scheduler()
