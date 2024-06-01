from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchBattlePods(Research):
    def __init__(self):
        super().__init__("Battle Pods", Technology.BATTLE_PODS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTroopPods(Research):
    def __init__(self):
        super().__init__("Troop Pods", Technology.TROOP_PODS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchSurvivalPods(Research):
    def __init__(self):
        super().__init__("Survival Pods", Technology.SURVIVAL_PODS, RESEARCH_POINTS, CATEGORY)
