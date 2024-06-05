from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchAndroidFarmers(Research):
    def __init__(self):
        super().__init__("Android Farmers ", Technology.ANDROID_FARMERS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAndroidWorkers(Research):
    def __init__(self):
        super().__init__("Android Workers", Technology.ANDROID_WORKERS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAndroidScientists(Research):
    def __init__(self):
        super().__init__("Android Scientists", Technology.ANDROID_SCIENTISTS, RESEARCH_POINTS, CATEGORY)
