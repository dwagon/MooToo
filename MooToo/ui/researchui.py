from MooToo.constants import Technology
from MooToo.ui.ui_util import get

RESEARCH_CACHE: dict[Technology:"ResearchUI"] = {}


#################################################################################################
def get_research(tech: "Technology") -> "ResearchUI":
    if tech not in RESEARCH_CACHE:
        research = get(f"/galaxy/research/{tech}")["research"]
        RESEARCH_CACHE[tech] = ResearchUI(**research)
    return RESEARCH_CACHE[tech]


#####################################################################################################
class ResearchUI:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.cost = kwargs["cost"]
        self.tag = kwargs["tag"]


# EOF
