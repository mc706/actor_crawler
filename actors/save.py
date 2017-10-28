import json

from thespian.actors import ActorTypeDispatcher, ActorExitRequest

from actors.messages import CrawlSaveMsg
from actors.decorator import log_arguments


class SaveActor(ActorTypeDispatcher):
    """
    Save Method
    """

    @log_arguments
    def receiveMsg_CrawlSaveMsg(self, message: CrawlSaveMsg, sender: ActorTypeDispatcher) -> None:
        """
        Message requesting data be saved
        """
        with open(f"{message.save_dir}/pages.json", "a") as report_file:
            report_file.write(json.dumps(message.data, indent=4) + ",\n")
