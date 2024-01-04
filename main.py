from dotenv import load_dotenv
load_dotenv()

from reddit_bot import RedditBot

def main():
    # Add the list of subreddits you'd like to add here
    subreddit_names = ["thelastdebuggernoban", "lastsubredditdebugger"]
    bot = RedditBot(subreddit_names)
    bot.start_streaming()

if __name__ == "__main__":
    main()