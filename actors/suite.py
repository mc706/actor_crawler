import os
import json
import logging

from thespian.actors import ActorTypeDispatcher, ActorExitRequest

from actors.messages import SiteRequestMsg, ConfigRequestMsg, ConfigResponseMsg, SiteStartMsg, SiteFinishMsg

log = logging.getLogger('thespian.log')


class SuiteActor(ActorTypeDispatcher):
    """
    Manages Suites
    """

    def __init__(self):
        super().__init__()
        self.sites = next(os.walk('sites'))[1]
        self.actors = {}
        log.debug('SuiteActor : ' + str(self.sites))

    def receiveMsg_SiteRequestMsg(self, message: SiteRequestMsg, sender) -> None:
        """
        Receive a request for to start a crawl
        """
        log.debug('SuiteActor[SiteRequestMsg] : ' + str(message))
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
        log.debug('SuiteActor[ConfigResponseMsg] : ' + str(message))
        self.send(sender, ActorExitRequest())
        if message.site:
            site_start_msg = SiteStartMsg(message.site)
            self.actors[message.site.key] = self.createActor('actors.site.SiteActor',
                                                             globalName='Site' + message.site.key)
            self.send(self.actors[message.site.key], site_start_msg)

    def receiveMsg_SiteFinishMsg(self, message: SiteFinishMsg, sender: ActorTypeDispatcher) -> None:
        """
        A site has finished running
        """
        log.debug('SuiteActor[SiteFinishMsg] : ' + str(message))
        with open(message.output_file, 'r') as output:
            raw_data = output.read()
            json_data = "[" + raw_data.rstrip(',\n') + "]"
            data = json.loads(json_data)
        with open(message.output_file, 'w') as output:
            output.write(json_data)
        print("Run Completed in {0:.2f}s".format(message.time_elapsed))
        print("{} urls scanned".format(len(data)))
        errors = [case for case in data if case['status_code'] != 200]
        if errors:
            print("{} Errors found:".format(len(errors)))
            for error in errors:
                print("{} | {}".format(error['status_code'], error['url']))
        else:
            print("No Errors Found During Run")
        with open(message.output_file.replace('pages.json', 'report.txt'), 'w') as report:
            report.write("Run Completed in {0:.2f}s\n".format(message.time_elapsed))
            report.write("{} urls scanned\n".format(len(data)))
            if errors:
                report.write("{} Errors found:\n".format(len(errors)))
                for error in errors:
                    report.write("{} | {}\n".format(error['status_code'], error['url']))
            else:
                report.write("No Errors Found During Run")
        self.send(sender, ActorExitRequest())

    def receiveMsg_ActorExitRequest(self, message: ActorExitRequest, sender):
        """
        Shutdown the sytem
        """
        log.debug('SuiteActor[ActorExitRequest]')
        for actor in self.actors:
            self.send(self.actors[actor], ActorExitRequest())
