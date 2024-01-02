from dotenv import load_dotenv
load_dotenv()

from reddit_bot import RedditBot

def main():
    bot = RedditBot(subreddit_name="debugmurica")
    bot.start_streaming()

if __name__ == "__main__":
    main()