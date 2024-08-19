import requests
from MooToo.ui.proxy.proxy_util import Proxy


#####################################################################################################
class ResearchProxy(Proxy):
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        data = self.get(self.url)["research"]
        self.name = data["name"]
        self.cost = data["cost"]
        self.tag = data["tag"]


# EOF
