from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchBattlePods(Research):
    def __init__(self):
        super().__init__("Battle Pods", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTroopPods(Research):
    def __init__(self):
        super().__init__("Troop Pods", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSurvivalPods(Research):
    def __init__(self):
        super().__init__("Survival Pods", RESEARCH_POINTS, CATEGORY)
