import yaml
from thespian.actors import ActorTypeDispatcher

from actors.messages import ConfigRequestMsg, ConfigResponseMsg
from actors.models import Site
from actors.decorator import log_arguments


class ConfigActor(ActorTypeDispatcher):
    """
    Load a Config
    """

    @log_arguments
    def receiveMsg_ConfigRequestMsg(self, message: ConfigRequestMsg, sender: ActorTypeDispatcher) -> None:
        """
        Load the requested config
        """
        try:
            with open(f"{message.directory}/config.yml", "r") as config_file:
                config = yaml.load(config_file)
                site = Site(**config)
                response = ConfigResponseMsg(site=site)
                self.send(sender, response)
        except IOError as ex:
            print('Config Error', ex)
            self.send(sender, ex)
