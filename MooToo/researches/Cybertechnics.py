from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchAndroidFarmers(Research):
    def __init__(self):
        super().__init__("Android Farmers ", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAndroidWorkers(Research):
    def __init__(self):
        super().__init__("Android Workers", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAndroidScientists(Research):
    def __init__(self):
        super().__init__("Android Scientists", RESEARCH_POINTS, CATEGORY)
