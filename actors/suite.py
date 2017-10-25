import os

from thespian.actors import ActorTypeDispatcher, ActorExitRequest

from actors.messages import SiteRequestMsg, ConfigRequestMsg, ConfigResponseMsg, SiteStartMsg
from actors.site import SiteActor


class SuiteActor(ActorTypeDispatcher):
    """
    Manages Suites
    """

    def __init__(self):
        super().__init__()
        self.sites = next(os.walk('sites'))[1]
        print('SuiteActor', self.sites)

    def receiveMsg_SiteRequestMsg(self, message: SiteRequestMsg, sender) -> None:
        """
        Receive a request for to start a crawl
        """
        print('SuiteActor[SiteRequestMsg]', message)
        if message.name and message.name in self.sites:
            suites = [message.name]
        else:
            suites = self.sites
        for suite in suites:
            config_msg = ConfigRequestMsg(directory=os.path.join('sites', suite))
            config_actor = self.createActor('actors.config.ConfigActor')
            self.send(config_actor, config_msg)

    def receiveMsg_ConfigResponseMsg(self, message: ConfigResponseMsg, sender: ActorTypeDispatcher) -> None:
        """
        Response from config actor
        """
        print('SuiteActor[ConfigResponseMsg]', message)
        self.send(sender, ActorExitRequest)
        if message.site:
            site_start_msg = SiteStartMsg(message.site)
            site_actor = self.createActor('actors.site.SiteActor', globalName='Site' + message.site.key)
            self.send(site_actor, site_start_msg)
