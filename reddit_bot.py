import os
import re
import praw
from pint import UnitRegistry

class RedditBot:
    def __init__(self, subreddit_name):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        self.subreddit = self.reddit.subreddit(subreddit_name)
        self.ureg = UnitRegistry()

        self.normalize_mapping = {
            "meters": "m", "meter": "m", "metre": "m", "metres": "m",
            "kilometers": "km", "kilometer": "km", "kilometre": "km", "kilometres": "km",
            "centimeters": "cm", "centimeter": "cm", "centimetre": "cm", "centimetres": "cm",
            "millimeters": "mm", "millimeter": "mm", "millimetre": "mm", "millimetres": "mm",
            "grams": "g", "gram": "g",
            "kilograms": "kg", "kilogram": "kg",
            "milligrams": "mg", "milligram": "mg",
            "centigrams": "cg", "centigram": "cg",
            "micrograms": "µg", "microgram": "µg",
            "liters": "l", "liter": "l", "litre": "l", "litres": "l",
            "milliliters": "ml", "milliliter": "ml", "millilitre": "ml", "millilitres": "ml",
            "celsius": "°C",
            "inches": "in", "inch": "in",
            "feet": "ft", "foot": "ft",
            "yards": "yd", "yard": "yd",
            "miles": "mi", "mile": "mi",
            "pounds": "lb", "pound": "lb",
            "ounces": "oz", "ounce": "oz",
            "tons": "ton", "ton": "ton",
            "quarts": "qt", "quart": "qt",
            "pints": "pt", "pint": "pt",
            "gallons": "gal", "gallon": "gal",
            "fluid ounces": "fl oz", "fluid ounce": "fl oz",
            "fahrenheit": "°F"
        }
        self.measurement_types = {
            "length": ["m", "km", "cm", "mm", "in", "ft", "yd", "mi"],
            "mass": ["g", "kg", "mg", "cg", "µg", "lb", "oz", "ton"],
            "volume": ["l", "ml", "cl", "dl", "qt", "pt", "gal", "fl oz"],
            "temperature": ["°C", "°F"]
        }
        self.imperial_types = {
            "length": ["in", "ft", "yd", "mi"],
            "mass": ["lb", "oz", "ton"],
            "volume": ["qt", "pt", "gal", "fl oz"],
            "temperature": ["°F"]
        }

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

        need_response = self.response_needed(metric_units, imperial_units)
        print(f"Need a response: {need_response}")

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

    def normalize_unit(self, unit):
        return self.normalize_mapping.get(unit.lower(), unit)

    def extract_units(self, text, patterns):
        units_data = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                value, unit = match[0], self.normalize_unit(match[2])
                units_data.append((value, unit))
        return units_data

    def response_needed(self, metric_units, imperial_units): 
        if len(metric_units) != len(imperial_units):
            return True
        
        for metric_tuple, imperial_tuple in zip(metric_units, imperial_units):
            metric_value, metric_unit = metric_tuple
            imperial_value, imperial_unit = imperial_tuple

            converted_to_imperial_value = self.convert_to_imperial(metric_value, metric_unit, imperial_unit)
            print(converted_to_imperial_value)
            if converted_to_imperial_value < 0 or not self.close_enough(float(converted_to_imperial_value), float(imperial_value)):
                return True
            
        return False

    def convert_to_imperial(self, metric_value, metric_unit, imperial_unit):
        if self.is_compatible(metric_unit, imperial_unit):
            try:
                metric_quantity = self.ureg(f"{metric_value} {metric_unit}")
                imperial_quantity = metric_quantity.to(imperial_unit)
                return imperial_quantity.magnitude
            except Exception as e:
                print(f"Error: {e}")
                return None
        else:
            print("Incompatible units")
            return -1

    def is_compatible(self, metric_unit, imperial_unit):
        for units in self.measurement_types.values():
            if metric_unit in units and imperial_unit in units:
                return True
        return False

    def close_enough(self, a, b):
        return abs(a - b) <= 3

