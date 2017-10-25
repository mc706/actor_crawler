from thespian.actors import ActorTypeDispatcher, ActorExitRequest

from actors.messages import CrawlRequestMsg, CrawlResponseMsg


class SiteActor(ActorTypeDispatcher):
    """
    Actor Responsible for Controlling the Site Crawling Session
    """
    def __init__(self, site: Site) -> None:
        super().__init__()
