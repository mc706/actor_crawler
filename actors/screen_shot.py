from urllib.parse import urlparse

from thespian.actors import ActorTypeDispatcher, ActorExitRequest
from thespian.troupe import troupe
from splinter import Browser

from actors.messages import ScreenShotRequestMsg
from actors.decorator import log_arguments


@troupe(25)
class ScreenShotActor(ActorTypeDispatcher):
    """
    Actor for taking screenshots
    """

    def __init__(self):
        super().__init__()
        self.browser = Browser('phantomjs')

    @log_arguments
    def receiveMsg_ScreenShotRequestMsg(self, message: ScreenShotRequestMsg, sender: ActorTypeDispatcher) -> None:
        """
        Receive a request for screens hot
        """
        image_name = ('/screen' + str(urlparse(message.url).path).replace('/', '_')).rstrip('_') + '.png'
        result_path = message.save_dir + image_name
        self.browser.visit(message.url)
        self.browser.driver.save_screenshot(result_path)

    @log_arguments
    def receiveMsg_ActorExitRequest(self, message: ActorExitRequest, sender: ActorTypeDispatcher):
        """
        Close Browser upon exit
        """
        self.browser.close()