# Twitter Scraper

A Python-based Twitter scraper that automatically scrapes tweets containing specific keywords every 24 hours without using the Twitter API.

## Features

- **Keyword-based scraping**: Scrapes tweets containing specified keywords
- **Automated scheduling**: Runs every 24 hours automatically
- **Data persistence**: Saves scraped tweets to CSV files
- **Duplicate prevention**: Automatically removes duplicate tweets
- **Comprehensive logging**: Detailed logs for monitoring and debugging
- **Configurable settings**: Easy customization through environment variables
- **Headless operation**: Can run in the background without GUI

## Project Structure

```
twitter_scraper/
├── scraper.py          # Main scraping logic
├── scheduler.py        # Scheduling and automation
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
├── .env.example      # Environment variables template
├── README.md         # This file
└── data/             # Directory for scraped data (created automatically)
    ├── scraped_tweets.csv
    └── scraper.log
```

## Installation

1. **Clone or download the project**
   ```bash
   cd twitter_scraper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome browser** (if not already installed)
   - The scraper uses Chrome WebDriver which will be automatically downloaded
   - Make sure Chrome browser is installed on your system

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to customize your keywords and settings.

## Configuration

### Environment Variables (.env file)

- `TWITTER_KEYWORDS`: Comma-separated list of keywords to search for
- `MAX_TWEETS_PER_KEYWORD`: Maximum number of tweets to scrape per keyword (default: 50)
- `SCRAPE_TIME`: Time to run daily scraping in 24-hour format (default: 09:00)
- `HEADLESS_MODE`: Run browser in headless mode (default: true)
- `BROWSER_TIMEOUT`: Browser timeout in seconds (default: 30)
- `SCROLL_PAUSE_TIME`: Pause time between scrolls in seconds (default: 2)
- `IMPLICIT_WAIT_TIME`: Implicit wait time for elements (default: 10)

### Default Keywords

If no environment variables are set, the scraper will use these default keywords:
- python
- machine learning
- AI
- data science
- programming

## Usage

### Run Once (for testing)
```bash
python scheduler.py --once
```

### Run with Scheduler (continuous operation)
```bash
python scheduler.py
```

### Run Scraper Directly
```bash
python scraper.py
```

## Output

### CSV File Structure
The scraped tweets are saved to `data/scraped_tweets.csv` with the following columns:

- `text`: Tweet content
- `username`: Twitter username
- `display_name`: User's display name
- `timestamp`: Tweet timestamp
- `url`: Direct link to the tweet
- `replies`: Number of replies
- `retweets`: Number of retweets
- `likes`: Number of likes
- `keyword`: The keyword that matched this tweet
- `scraped_at`: When the tweet was scraped

### Log Files
Detailed logs are saved to `data/scraper.log` and also displayed in the console.

## Running as a Service

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily"
4. Set action to start the Python script: `python C:\path\to\twitter_scraper\scheduler.py`

### Linux/Mac (Cron)
Add to crontab:
```bash
# Run at 9:00 AM daily
0 9 * * * cd /path/to/twitter_scraper && python scheduler.py --once
```

### Docker (Optional)
Create a Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

COPY . .
CMD ["python", "scheduler.py"]
```

## Important Notes

### Legal and Ethical Considerations
- **Respect Twitter's Terms of Service**: This scraper is for educational purposes
- **Rate Limiting**: The scraper includes delays to avoid overwhelming Twitter's servers
- **Data Privacy**: Be mindful of the data you collect and how you use it
- **Robots.txt**: Consider Twitter's robots.txt file

### Technical Limitations
- **Dynamic Content**: Twitter heavily uses JavaScript, so Selenium is required
- **Rate Limiting**: Twitter may block requests if too frequent
- **Layout Changes**: Twitter's layout changes may break selectors
- **Login Requirements**: Some content may require authentication

### Troubleshooting

1. **Chrome Driver Issues**
   - The script automatically downloads the correct ChromeDriver
   - Ensure Chrome browser is installed and up to date

2. **Timeout Errors**
   - Increase `BROWSER_TIMEOUT` in .env file
   - Check internet connection
   - Twitter might be blocking requests

3. **No Tweets Found**
   - Check if keywords are too specific
   - Verify Twitter search results manually
   - Twitter's search algorithm may limit results

4. **Memory Issues**
   - Reduce `MAX_TWEETS_PER_KEYWORD`
   - Run in headless mode
   - Close other applications

## Customization

### Adding New Data Fields
Modify the `extract_tweet_data` method in `scraper.py` to extract additional information.

### Changing Search Parameters
Modify the `TWITTER_SEARCH_URL` in `config.py` to change search parameters (e.g., recent tweets, popular tweets).

### Custom Scheduling
Modify `scheduler.py` to implement custom scheduling logic.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes only. Please respect Twitter's Terms of Service and applicable laws.
