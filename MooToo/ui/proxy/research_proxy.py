from MooToo.constants import Technology
from MooToo.ui.proxy.proxy_util import get

RESEARCH_CACHE: dict[Technology:"ResearchProxy"] = {}


#################################################################################################
def get_research(tech: "Technology") -> "ResearchProxy":
    if tech not in RESEARCH_CACHE:
        research = get(f"/galaxy/research/{tech}")["research"]
        RESEARCH_CACHE[tech] = ResearchProxy(**research)
    return RESEARCH_CACHE[tech]


#####################################################################################################
class ResearchProxy:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.cost = kwargs["cost"]
        self.tag = kwargs["tag"]


# EOF
