from dotenv import load_dotenv
load_dotenv()

from reddit_bot import RedditBot

def main():
    subreddit_names = ["pleasedontbanmedebug", "rlydontbanmedebug"]
    bot = RedditBot(subreddit_names)
    bot.start_streaming()

if __name__ == "__main__":
    main()