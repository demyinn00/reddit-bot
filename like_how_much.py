import random
from pint import UnitRegistry

class LikeHowMuch: 
    def __init__(self):
        self.ureg = UnitRegistry()

        # in meters
        self.length_examples = {
            "sheet of paper": {"value": 0.0001, "singular": "the thickness of a sheet of paper", "plural": "sheets of paper stacked vertically", "phrase": ""},
            "US penny": {"value": 0.00152, "singular": "the thickness of a US penny", "plural": "US pennies stacked vertically", "phrase": ""},
            "slice of bread": {"value": 0.0127, "singular": "the thickness of a slice of bread", "plural": "slices of bread laid end to end", "phrase": ""},
            "Mona Lisa": {"value": 0.772, "singular": "of the height of the Mona Lisa", "plural": "Mona Lisas tall", "phrase": ""},
            "Aang's Staff": {"value": 1.8, "singular": "of Aang's staff from Avatar", "plural": "Aang's staffs", "phrase": ""},
            "Voldemort": {"value": 1.94, "singular": "Voldemort", "plural": "Voldemorts", "phrase": ""},
            "giraffe": {"value": 5.3, "singular": "giraffe", "plural": "giraffes", "phrase": ""},
            "Attack Titan": {"value": 15, "singular": "Attack Titan", "plural": "Attack Titans", "phrase": ""},
            "Colossal Titan": {"value": 60, "singular": "Colossal Titan", "plural": "Colossal Titans", "phrase": ""}
        }

        # in grams
        self.mass_examples = {
            "single eyelash": {"value": 0.00017, "singular": "single eyelash", "plural": "single eyelashes", "phrase": ""},
            "average ant": {"value": 0.0025, "singular": "average ant", "plural": "average ants", "phrase": ""},
            "iPhone 15": {"value": 171, "singular": "iPhone 15", "plural": "iPhone 15s", "phrase": ""},
            "toilet paper roll": {"value": 227, "singular": "toilet paper roll", "plural": "toilet paper rolls", "phrase": ""},
            "empty hydro flask": {"value": 499, "singular": "empty 40 oz hydro flask", "plural": "empty 40 oz hydro flasks", "phrase": ""},
            "average raccoon": {"value": 22000, "singular": "average raccoon", "plural": "average raccoons", "phrase": ""},
            "average panda": {"value": 110000, "singular": "average panda", "plural": "average pandas", "phrase": ""},
            "Charizard": {"value": 90718.5, "singular": "Charizard", "plural": "Charizards", "phrase": ""},
            "Mercedes Benz": {"value": 1814369, "singular": "Mercedes Benz", "plural": "Mercedes Benzes", "phrase": ""}
        }

        # in liters
        self.volume_examples = {
            "soda can": {"value": 0.355, "singular": "soda can", "plural": "soda cans", "phrase": ""},
            "basketball": {"value": 7.5, "singular": "basketball", "plural": "basketballs", "phrase": ""},
            "car gas tank": {"value": 55, "singular": "car gas tank", "plural": "car gas tanks", "phrase": ""},
            "bathtub": {"value": 175, "singular": "average bathtub", "plural": "average bathtubs", "phrase": ""},
            "home fridge": {"value": 600, "singular": "average home fridge", "plural": "average home fridges", "phrase": ""},
            "Reflecting Pool": {"value": 10000, "singular": "Reflecting Pool at Lincoln Memorial", "plural": "Reflecting Pools at Lincoln Memorial", "phrase": ""},
            "Water tanker truck": {"value": 30000, "singular": "water tanker truck", "plural": "water tanker trucks", "phrase": ""},
            "Olympic pool": {"value": 2500000, "singular": "olympic swimming pool", "plural": "olympic swimming pools", "phrase": ""},
            "Lake Baikal": {"value": 23600000000000, "singular": "Lake Baikal in Siberia", "plural": "Lake Baikals in Siberia", "phrase": ""}
        }

        # in Celsius
        self.temperature_examples = {
            "Body Temperature": {"value": 37, "singular": "of the human body's temperature", "plural": "times the human body's temperature", "phrase": ""},
            "Boiling Point": {"value": 100, "singular": "of water's boiling point", "plural": "times water's boiling point", "phrase": ""},
            "Lead Melting Point": {"value": 327.5, "singular": "of lead's melting point", "plural": "times hotter than lead's melting point", "phrase": ""},
            "Lava": {"value": 1000, "singular": "of lava's temperature", "plural": "times lava's temperature", "phrase": ""},
            "Sun Surface": {"value": 5500, "singular": "of the sun's surface", "plural": "times hotter than the sun's surface", "phrase": ""}
        }


    def get_random_conversion(self, examples, input_value):
        _, example_data = random.choice(list(examples.items()))
        compare_value = input_value / example_data["value"]
        unit_form = example_data["plural"] if compare_value > 1 else example_data["singular"]
        return f"That's like {compare_value:4f} {unit_form}!"

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
