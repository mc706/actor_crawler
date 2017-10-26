import json
import logging

from thespian.actors import ActorTypeDispatcher, ActorExitRequest


from actors.messages import CrawlSaveMsg

log = logging.getLogger('thespian.log')

class SaveActor(ActorTypeDispatcher):
    """
    Save Method
    """

    def receiveMsg_CrawlSaveMsg(self, message: CrawlSaveMsg, sender: ActorTypeDispatcher) -> None:
        """
        Message requesting data be saved
        """
        log.debug("SaveActor[CrawlSaveMsg] : " + str(message))
        with open(f"{message.save_dir}/pages.json", "a") as report_file:
            report_file.write(json.dumps(message.data, indent=4) + ",\n")
