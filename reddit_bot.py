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
        print("Metric Units Detected:", metric_units)

        imperial_units = self.detect_imperial(comment.body)
        print("Imperial Units Detected:", imperial_units)

    def detect_metric(self, text):
        length_pattern = r"\b(\d+(\.\d+)?)\s?(m|meter|metre|kilometer|kilometre|centimeter|centimetre|millimeter|millimetre|km|cm|mm)s?\b"
        mass_pattern = r"\b(\d+(\.\d+)?)\s?(g|gram|kilogram|milligram|centigram|microgram|kg|mg|cg|µg)s?\b"
        volume_pattern = r"\b(\d+(\.\d+)?)\s?(l|liter|litre|milliliter|millilitre|cl|dl|ml)s?\b"
        temperature_pattern = r"\b(\d+(\.\d+)?)\s?°?C\b|celsius\b"

        return self.extract_units(text, [length_pattern, mass_pattern, volume_pattern, temperature_pattern])

    def detect_imperial(self, text):
        length_pattern = r"\b(\d+(\.\d+)?)\s?(in|inch|inches|ft|foot|feet|yd|yard|yards|mi|mile|miles)s?\b"
        mass_pattern = r"\b(\d+(\.\d+)?)\s?(lb|lbs|pound|pounds|oz|ounce|ounces|ton|tons)s?\b"
        volume_pattern = r"\b(\d+(\.\d+)?)\s?(qt|quart|quarts|pt|pint|pints|gal|gallon|gallons|fl oz|fluid ounce|fluid ounces)s?\b"
        temperature_pattern = r"\b(\d+(\.\d+)?)\s?°?F\b|fahrenheit\b"

        return self.extract_units(text, [length_pattern, mass_pattern, volume_pattern, temperature_pattern])

    def extract_units(self, text, patterns):
        units_data = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                value, unit = match[0], match[2]
                units_data.append((value, unit))
        return units_data