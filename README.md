# Reddit Metric Conversion Bot

## Description
This project is a Reddit bot designed to automatically detect and respond to comments containing metric measurements in specified subreddits. The bot converts these measurements into imperial units and provides fun, relatable comparisons to help illustrate the converted measurements. It aims to enhance understanding and engagement in discussions involving different measurement systems.

## Setup

### Installation
1. Clone the repository:
```
git clone https://github.com/demyinn00/reddit-bot.git
```
2. Install required Python packages:
```
pip install -r requirements.txt
```
3. Set up Reddit API credentials:
- Create a Reddit account and a new Reddit application in [Reddit preferences](https://www.reddit.com/prefs/apps) to get your `client_id` and `client_secret`.
- Set the following environment variables with your Reddit API credentials and bot account details:
```
REDDIT_CLIENT_ID='your_client_id'
REDDIT_CLIENT_SECRET='your_client_secret'
REDDIT_USER_AGENT='bot_user_agent'
REDDIT_USERNAME='your_bot_username'
REDDIT_PASSWORD='your_bot_password'
```
### Running the Bot
Execute the main script to start the bot:
```
python3 main.py
```

## Known Issues
- **API Rate Limiting**: Extensive use of the Reddit API, especially during development and testing, can lead to hitting the rate limits imposed by Reddit. This can temporarily block the bot from accessing Reddit data.
- **Subreddit Accessibility**: The bot may encounter issues if it tries to access a subreddit that is private, restricted, or banned.
  - It also might get flagged for spamming (I've gottne banned multiple times...)
  - I found that it works best on a subreddit owned by the bot's reddit acccount, but it does work on other subreddits. Just be warned, your bot might get shadowbanned. 
- **Unit Conversion Limitations**: The bot currently handles a predefined set of metric units. It may not recognize or correctly convert units that are not explicitly defined in its configuration.
  - The main units that it recognizes (in most both abbreviated and non-abbreviated formats) are: 
    - metrics: milli, centi, base (gram, liter, etc.), kilo; c, celsius
    - imperial: oz, lb, ton, in, yd, mi, pt, qt, gal; f, fahrenheit
    - Handles pluralized and singular
    - Case-insensitive
- **Temperature Conversion**: There have been occasional issues with detecting and converting temperature units, especially when the unit is not explicitly mentioned. 
  - For temperature, it only recognizes these patterns:
    - 100 c, 100 C, 100 celsius, 100 Celsius
    - Same for fahrenheit 
    - It has trouble extracting the units if the word degrees is present. I'm unsure if it's due to the regex or the `extract_units` method. 
