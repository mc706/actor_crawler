from thespian.actors import ActorTypeDispatcher, ActorExitRequest
import yaml

from actors.messages import CrawlSaveMsg


class SaveActor(ActorTypeDispatcher):
    """
    Save Method
    """

    def receiveMsg_CrawlSaveMsg(self, message: CrawlSaveMsg, sender: ActorTypeDispatcher) -> None:
        """
        Message requesting data be saved
        """
        print("SaveActor[CrawlSaveMsg]", message)
        with open(f"{message.save_dir}/pages.yml", "a") as report_file:
            report_file.write(yaml.dump(message.data, default_flow_style=False))
