import os
import threading
import re
import praw
from pint import UnitRegistry

class RedditBot:
    def __init__(self, subreddit_names):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        self.subreddits = [self.reddit.subreddit(name) for name in subreddit_names]
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
            "fluid ounces": "imperial_fluid_ounce", "fluid ounce": "imperial_fluid_ounce",
            "fahrenheit": "°F"
        }
        self.measurement_types = {
            "length": ["m", "km", "cm", "mm", "in", "ft", "yd", "mi"],
            "mass": ["g", "kg", "mg", "cg", "µg", "lb", "oz", "ton"],
            "volume": ["l", "ml", "cl", "dl", "qt", "pt", "gal", "fl oz", "imperial_fluid_ounce"],
            "temperature": ["°C", "°F"]
        }
        self.imperial_types = {
            "length": ["in", "ft", "yd", "mi"],
            "mass": ["oz", "lb", "ton"],
            "volume": ["imperial_fluid_ounce", "pt", "qt", "gal"],
            "temperature": ["°F"]
        }

    def start_streaming(self):
        try:
            threads = []
            for subreddit in self.subreddits:
                thread = threading.Thread(target=self.monitor_subreddit, args=(subreddit,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print("Bot stopped manually.")

    def monitor_subreddit(self, subreddit):
        print(subreddit.display_name)
        for comment in subreddit.stream.comments(skip_existing=True):
            self.process_comment(comment)

    def process_comment(self, comment):
        metric_units = self.detect_metric(comment.body)
        print("Metric Units Detected:", metric_units)

        imperial_units = self.detect_imperial(comment.body)
        print("Imperial Units Detected:", imperial_units)

        need_response = self.response_needed(metric_units, imperial_units)
        print(f"Need a response: {need_response}")

        if need_response: 
            response_text = self.generate_response(metric_units)
            print(f"Response: {response_text}")
            self.respond_to_comment(comment, response_text)

    def respond_to_comment(self, comment, response_text):
        return 0

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
        if len(metric_units) == 0:
            return False

        if len(metric_units) != len(imperial_units):
            return True

        for metric_tuple, imperial_tuple in zip(metric_units, imperial_units):
            metric_value, metric_unit = metric_tuple
            imperial_value, imperial_unit = imperial_tuple

            converted_to_imperial_value = self.convert_to_imperial(metric_value, metric_unit, imperial_unit)
            print(converted_to_imperial_value)
            if converted_to_imperial_value is None or not self.close_enough(float(converted_to_imperial_value), float(imperial_value)):
                return True
            
        return False

    def generate_response(self, metric_units):
        responses = []
        for metric_value, metric_unit in metric_units:
            best_conversion = self.find_best_conversion(metric_value, metric_unit)
            if best_conversion:
                imperial_value, imperial_unit = best_conversion
                responses.append(f"{metric_value} {metric_unit} is {imperial_value} {imperial_unit}")
        return " ".join(responses)

    def find_best_conversion(self, metric_value, metric_unit):
        last_pair = tuple()

        for measurement, units in self.imperial_types.items():
            if metric_unit in self.measurement_types[measurement]:
                for imperial_unit in units:
                    converted_to_imperial_value = self.convert_to_imperial(metric_value, metric_unit, imperial_unit)
                    if converted_to_imperial_value is None:
                        return None
                    elif converted_to_imperial_value < 1:
                        return last_pair
                    else: 
                        print(f"in the else statement: {last_pair} {imperial_unit}")
                        last_pair = (round(converted_to_imperial_value, 2), imperial_unit)
                        print(f"in the else statement: {last_pair} {imperial_unit}")

        return last_pair

    def convert_to_imperial(self, metric_value, metric_unit, imperial_unit):
        if self.is_compatible(metric_unit, imperial_unit):
            try:
                metric_quantity = self.ureg(f"{metric_value} {metric_unit}")
                imperial_quantity = metric_quantity.to(imperial_unit)
                return imperial_quantity.magnitude
            except Exception as e:
                print(f"Error converting {metric_value} {metric_unit} to {imperial_unit}: {e}")
                return None
        else:
            print("Incompatible units")
            return None

    def is_compatible(self, metric_unit, imperial_unit):
        for units in self.measurement_types.values():
            if metric_unit in units and imperial_unit in units:
                return True
        return False

    def close_enough(self, a, b):
        return abs(a - b) <= 3

