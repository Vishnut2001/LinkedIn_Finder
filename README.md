**LinkedIn Profile Finder (Selenium-based)**

This script automates LinkedIn profile lookups using names, designations, and organizations provided in a CSV file. Ideal for events, networking, and B2B lead generation.

🔧 Features

Google or Bing based LinkedIn search

Handles CAPTCHA with manual support

Supports resuming partial runs

Avoids bot detection with undetected Chromedriver

📁 Files

main.py: Core logic for searching and writing results

Exhibitors Subset.csv: Input file with data to process

contacts_with_linkedin.csv: Output with LinkedIn profiles

✅ Requirements

pip install selenium webdriver-manager undetected-chromedriver

🚀 Run It

python main.py

Follow the prompts to enter row ranges and search preferences.

🧠 Notes

Manual CAPTCHA solving required

Adds random delays to reduce detection

Start/stop anytime without overwriting past results

📄 License

MIT License — For personal or educational use only.
