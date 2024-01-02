import os
import re
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
        metric_units = self.detect_metric(comment.body)
        print(metric_units)

    def detect_metric(self, text):
        meter_pattern = r"\b(\d+(\.\d+)?)\s?(m|meter|metre|kilometer|kilometre|centimeter|centimetre|millimeter|millimetre|km|cm|mm)s?\b"
        gram_pattern = r"\b(\d+(\.\d+)?)\s?(g|gram|kilogram|milligram|centigram|microgram|kg|mg|cg|µg)s?\b"
        liter_pattern = r"\b(\d+(\.\d+)?)\s?(l|liter|litre|milliliter|millilitre|centiliter|centilitre|microliter|microlitre|ml|cl|µl)s?\b"
        celsius_pattern = r"\b(\d+(\.\d+)?)\s?°?C\b|celsius\b"

        metric_data = []
        for pattern in [meter_pattern, gram_pattern, liter_pattern, celsius_pattern]:
            matches = re.findall(pattern, text)
            for match in matches:
                value, unit = match[0], ''.join(match[1:])
                metric_data.append((value, unit))

        return metric_data
