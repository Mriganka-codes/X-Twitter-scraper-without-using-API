import time
import logging
import pandas as pd
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
from config import Config

class TwitterScraper:
    def __init__(self):
        self.setup_logging()
        self.setup_data_directory()
        self.driver = None

    def setup_logging(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_data_directory(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)

    def setup_driver(self):
        try:
            chrome_options = Options()
            if Config.HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            webdriver_path = r"D:\attachments\chromedriver-win64\chromedriver-win64\chromedriver.exe"
            service = Service(executable_path=webdriver_path)
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(Config.IMPLICIT_WAIT_TIME)
            self.logger.info("WebDriver setup successful")
            
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise
    
    def login(self):
        """Automates the login process for Twitter/X."""
        try:
            self.driver.get("https://x.com/login")
            
            username_input = WebDriverWait(self.driver, Config.BROWSER_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="text"]'))
            )
            username_input.send_keys(Config.TWITTER_USERNAME)
            self.driver.find_element(By.XPATH, '//span[text()="Next"]').click()
            self.logger.info("Username entered.")
            
            password_input = WebDriverWait(self.driver, Config.BROWSER_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            password_input.send_keys(Config.TWITTER_PASSWORD)
            self.driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
            self.logger.info("Password entered.")

            WebDriverWait(self.driver, Config.BROWSER_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]'))
            )
            self.logger.info("Login successful!")

        except TimeoutException:
            self.logger.error("Login failed. Check your credentials or the website structure.")
            raise
        except Exception as e:
            self.logger.error(f"An error occurred during login: {e}")
            raise

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")

    def extract_tweet_data(self, tweet_element):
        """Extracts data from a single tweet element, handling stale elements."""
        try:
            # Re-find elements within the try-except block to ensure they are fresh
            tweet_data = {}
            
            # Extract URL and Timestamp
            time_element = tweet_element.find_element(By.CSS_SELECTOR, 'a time')
            link_element = time_element.find_element(By.XPATH, '..')
            tweet_data['url'] = link_element.get_attribute('href')
            tweet_data['timestamp'] = time_element.get_attribute('datetime')

            # Extract Text
            text_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            tweet_data['text'] = text_element.text
            
            # Add placeholders for other data
            #tweet_data['username'] = "N/A"
            #tweet_data['display_name'] = "N/A"
            #tweet_data['replies'] = "0"
            #tweet_data['retweets'] = "0"
            #tweet_data['likes'] = "0"
            #tweet_data['scraped_at'] = datetime.now().isoformat()
            
            return tweet_data
        
        except StaleElementReferenceException:
            # This happens if the element gets removed from the page while we are processing it.
            # We just log it and move on.
            self.logger.warning("Encountered a stale element, skipping it.")
            return None
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during data extraction: {e}")
            return None

    def scrape_tweets_for_keyword(self, keyword):
        """Scrapes tweets for a keyword, handling scrolling and data extraction robustly."""
        self.logger.info(f"Scraping tweets for keyword: {keyword}")
        
        try:
            search_url = Config.TWITTER_SEARCH_URL.format(keyword.replace(' ', '%20'))
            self.driver.get(search_url)
            
            WebDriverWait(self.driver, Config.BROWSER_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, 'article'))
            )
            
            tweets_data = []
            processed_urls = set() # Keep track of URLs we have already processed
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            patience = 3
            patience_counter = 0

            while len(tweets_data) < Config.MAX_TWEETS_PER_KEYWORD:
                # Find all tweet articles currently on the page
                current_tweets_on_page = self.driver.find_elements(By.TAG_NAME, 'article')
                
                # Process each tweet element
                for tweet_element in current_tweets_on_page:
                    data = self.extract_tweet_data(tweet_element)
                    
                    # Check if data was extracted and if we haven't processed this URL before
                    if data and data['url'] not in processed_urls:
                        data['keyword'] = keyword
                        tweets_data.append(data)
                        processed_urls.add(data['url'])
                        self.logger.info(f"Collected {len(tweets_data)}/{Config.MAX_TWEETS_PER_KEYWORD} tweets.")
                
                # Check if we have enough tweets
                if len(tweets_data) >= Config.MAX_TWEETS_PER_KEYWORD:
                    break
                
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(Config.SCROLL_PAUSE_TIME)
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    patience_counter += 1
                    if patience_counter >= patience:
                        self.logger.info("Reached end of page or no new content is loading.")
                        break
                else:
                    patience_counter = 0
                last_height = new_height

            self.logger.info(f"Finished scraping for '{keyword}'. Found {len(tweets_data)} tweets.")
            return tweets_data
            
        except TimeoutException:
            self.logger.error(f"Initial page load timed out for keyword: {keyword}.")
            return []
        except Exception as e:
            self.logger.error(f"A critical error occurred while scraping for '{keyword}': {e}")
            return []


    def save_tweets_to_csv(self, all_tweets_data):
        if not all_tweets_data:
            self.logger.warning("No tweets to save")
            return
            
        df = pd.DataFrame(all_tweets_data)
        
        if os.path.exists(Config.TWEETS_FILE):
            existing_df = pd.read_csv(Config.TWEETS_FILE)
            df = pd.concat([existing_df, df], ignore_index=True)
            
        df.drop_duplicates(subset=['url'], keep='last', inplace=True)
        
        df.to_csv(Config.TWEETS_FILE, index=False)
        self.logger.info(f"Saved {len(df)} unique tweets to {Config.TWEETS_FILE}")
        
    def run_scraping_session(self):
        self.logger.info("Starting Twitter scraping session")
        try:
            self.setup_driver()
            self.login()
            keywords = Config.get_keywords_from_env()
            all_tweets_data = []
            
            for keyword in keywords:
                tweets_data = self.scrape_tweets_for_keyword(keyword)
                all_tweets_data.extend(tweets_data)
                time.sleep(5)
                
            self.save_tweets_to_csv(all_tweets_data)
            self.logger.info(f"Scraping session completed.")
            
        except Exception as e:
            self.logger.error(f"Error during scraping session: {str(e)}")
        finally:
            self.close_driver()

if __name__ == "__main__":
    scraper = TwitterScraper()
    scraper.run_scraping_session()