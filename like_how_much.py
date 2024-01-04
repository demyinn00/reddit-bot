import random
from pint import UnitRegistry

class LikeHowMuch: 
    def __init__(self):
        self.ureg = UnitRegistry()

        # in meters
        self.length_examples = {
            "sheet of paper": {"value": 0.0001, "singular": "sheet of paper", "plural": "sheets of paper", "phrase": "stacked vertically"},
            "US penny": {"value": 0.00152, "singular": "US penny", "plural": "US pennies", "phrase": "stacked vertically"},
            "slice of bread": {"value": 0.0127, "singular": "slice of bread", "plural": "slices of bread", "phrase": "laid end to end"},
            "Mona Lisa": {"value": 0.772, "singular": "Mona Lisa", "plural": "Mona Lisas", "phrase": "tall"},
            "Aang's Staff": {"value": 1.8, "singular": "Aang's Staff", "plural": "Aang's Staffs", "phrase": "long"},
            "Voldemort": {"value": 1.94, "singular": "Voldemort", "plural": "Voldemorts", "phrase": "tall"},
            "giraffe": {"value": 5.3, "singular": "giraffe", "plural": "giraffes", "phrase": "tall"},
            "Attack Titan": {"value": 15, "singular": "Attack Titan", "plural": "Attack Titans", "phrase": "tall"},
            "Colossal Titan": {"value": 60, "singular": "Colossal Titan", "plural": "Colossal Titans", "phrase": "tall"}
        }

        # in grams
        self.mass_examples = {
            "single eyelash": {"value": 0.00017, "singular": "single eyelash", "plural": "single eyelashes", "phrase": "heavy"},
            "average ant": {"value": 0.0025, "singular": "average ant", "plural": "average ants", "phrase": "heavy"},
            "iPhone 15": {"value": 171, "singular": "iPhone 15", "plural": "iPhone 15s", "phrase": "heavy"},
            "toilet paper roll": {"value": 227, "singular": "toilet paper roll", "plural": "toilet paper rolls", "phrase": "heavy"},
            "empty hydro flask": {"value": 499, "singular": "empty 40 oz hydro flask", "plural": "empty 40 oz hydro flasks", "phrase": "heavy"},
            "average raccoon": {"value": 22000, "singular": "average raccoon", "plural": "average raccoons", "phrase": "heavy"},
            "average panda": {"value": 110000, "singular": "average panda", "plural": "average pandas", "phrase": "heavy"},
            "Charizard": {"value": 90718.5, "singular": "Charizard", "plural": "Charizards", "phrase": "heavy"},
            "Mercedes Benz": {"value": 1814369, "singular": "Mercedes Benz", "plural": "Mercedes Benzes", "phrase": "heavy"}
        }

        # in liters
        self.volume_examples = {
            "soda can": {"value": 0.355, "singular": "soda can", "plural": "soda cans", "phrase": "full"},
            "basketball": {"value": 7.5, "singular": "basketball", "plural": "basketballs", "phrase": "inflated"},
            "car gas tank": {"value": 55, "singular": "car gas tank", "plural": "car gas tanks", "phrase": "full"},
            "bathtub": {"value": 175, "singular": "average bathtub", "plural": "average bathtubs", "phrase": "full"},
            "home fridge": {"value": 600, "singular": "average home fridge", "plural": "average home fridges", "phrase": "volume"},
            "Reflecting Pool": {"value": 10000, "singular": "Reflecting Pool at Lincoln Memorial", "plural": "Reflecting Pools at Lincoln Memorial", "phrase": "full"},
            "Water tanker truck": {"value": 30000, "singular": "water tanker truck", "plural": "water tanker trucks", "phrase": "full"},
            "Olympic pool": {"value": 2500000, "singular": "Olympic swimming pool", "plural": "Olympic swimming pools", "phrase": "full"},
            "Lake Baikal": {"value": 23600000000000, "singular": "Lake Baikal in Siberia", "plural": "Lake Baikals in Siberia", "phrase": "volume"}
        }

        # in Celsius
        self.temperature_examples = {
            "Liquid Nitrogen": {"value": -196, "singular": "Liquid Nitrogen", "plural": "Liquid Nitrogen", "phrase": "cold"},
            "Dry Ice": {"value": -78.5, "singular": "Dry Ice", "plural": "Dry Ice", "phrase": "cold"},
            "Siberian Winter": {"value": -50, "singular": "Winter in Siberia", "plural": "Winters in Siberia", "phrase": "cold"},
            "Freezing Point": {"value": 0, "singular": "Water freezing point", "plural": "Water freezing points", "phrase": "cold"},
            "Body Temperature": {"value": 37, "singular": "Human Body Temperature", "plural": "Human Body Temperatures", "phrase": "warm"},
            "Boiling Point": {"value": 100, "singular": "Water boiling point", "plural": "Water boiling points", "phrase": "hot"},
            "Lead Melting Point": {"value": 327.5, "singular": "Melting Point of Lead", "plural": "Melting Points of Lead", "phrase": "hot"},
            "Lava": {"value": 1000, "singular": "Lava", "plural": "Lava", "phrase": "hot"},
            "Sun Surface": {"value": 5500, "singular": "Surface of the Sun", "plural": "Surfaces of the Sun", "phrase": "extremely hot"}
        }


    def get_random_conversion(self, examples, input_value):
        _, example_data = random.choice(list(examples.items()))
        compare_value = input_value / example_data["value"]
        unit_form = example_data["plural"] if compare_value > 1 else example_data["singular"]
        return f"That's like {compare_value:4f} {unit_form} {example_data['phrase']}!"

    def compare_length(self, value, unit):
        meters = self.convert_to_standard_metric(value, unit, "length")
        return self.get_random_conversion(self.length_examples, meters)
    
    def compare_mass(self, value, unit): 
        grams = self.convert_to_standard_metric(value, unit, "mass")
        return self.get_random_conversion(self.mass_examples, grams)
    
    def compare_volume(self, value, unit): 
        liters = self.convert_to_standard_metric(value, unit, "volume")
        return self.get_random_conversion(self.volume_examples, liters)
    
    def compare_temperature(self, value, unit):
        celsius = self.convert_to_standard_metric(value, unit, "temperature")
        return self.get_random_conversion(self.temperature_examples, celsius)

    def convert_to_standard_metric(self, value, unit, measurement):
        quantity = self.ureg.Quantity(value, unit)

        if measurement == "length":
            return quantity.to(self.ureg.meter).magnitude
        elif measurement == "mass":
            return quantity.to(self.ureg.gram).magnitude
        elif measurement == "volume":
            return quantity.to(self.ureg.liter).magnitude
        elif measurement == "temperature":
            return quantity.to(self.ureg.celsius).magnitude
        else:
            raise ValueError(f"Error: unknown measurement {measurement}")
