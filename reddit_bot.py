import os
import praw

class RedditBot:
    def __init__(self, subreddit_name):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        self.subreddit = self.reddit.subreddit(subreddit_name)

    def start_streaming(self):
        try:
            print(self.subreddit)
            for comment in self.subreddit.stream.comments(skip_existing=True):
                self.process_comment(comment)
        except KeyboardInterrupt:
            print("Bot stopped manually.")

    def process_comment(self, comment):
        print(comment.body)
