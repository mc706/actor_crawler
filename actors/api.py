from thespian.actors import ActorTypeDispatcher, ActorExitRequest

from actors.messages import *
from actors.decorator import log_arguments


class APIActor(ActorTypeDispatcher):
    """
    Handles requests from API
    """

    @log_arguments
    def receiveMsg_APIListSitesMsg(self, message: APIListListMsg, sender) -> None:
        """
        Handle a get the list of sites message
        """
        pass

    @log_arguments
    def receiveMsg_APICreateSiteMsg(self, message: APICreateSiteMsg, sender) -> None:
        """
        Handle request to create a new site
        """
        pass

    @log_arguments
    def receiveMsg_APISiteDetailMsg(self, message: APISiteDetailMsg, sender) -> None:
        """
        Get Site Detail
        """
        pass

    @log_arguments
    def receiveMsg_APIStartSiteCrawlMsg(self, message: APIStartSiteCrawlMsg, sender) -> None:
        """
        Start a craw of a site
        """
        pass

    @log_arguments
    def receiveMsg_APIGetCrawlMsg(self, message: APIGetCrawlMsg, sender) -> None:
        """
        Get crawl
        """
        pass

    @log_arguments
    def receiveMsg_ActorExitRequest(self, message: ActorExitRequest, sender) -> None:
        """
        Shutdown
        """
        pass
