""" Buildings"""


#####################################################################################################
class Building:
    """Building"""

    def __init__(self, name):
        self.name = name
        self.maintenance = 0
        self.cost = 0

    def __str__(self):
        return self.name

    def food_bonus(self) -> int:
        return 0

    def prod_bonus(self) -> int:
        return 0


#####################################################################################################
class HydroponicFarm(Building):
    def __init__(self):
        super().__init__("Hydroponic Farm")
        self.maintenance = 2
        self.cost = 60

    def food_bonus(self) -> int:
        return 2


#####################################################################################################
class AutomatedFactory(Building):
    def __init__(self):
        super().__init__("Automated Factory")
        self.maintenance = 2
        self.cost = 60

    def prod_bonus(self) -> int:
        return 2
