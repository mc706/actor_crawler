from typing import List, Set

from actors.models import Site


class BaseMsg:
    """
    Base Message
    """

    def __str__(self):
        return "message: {}".format(self.__dict__)


class SiteRequestMsg(BaseMsg):
    """
    Site Requested
    """

    def __init__(self, name: str = None):
        self.name = name


class ConfigRequestMsg(BaseMsg):
    """
    Request for configuration

    SuiteActor -> ConfigActor
    """

    def __init__(self, directory: str) -> None:
        self.directory = directory


class ConfigResponseMsg(BaseMsg):
    """
    Response for configuration.

    ConfigActor -> SuiteActor
    """

    def __init__(self, site: Site):
        self.site = site


class SiteStartMsg(BaseMsg):
    """
    Start a site
    """

    def __init__(self, site: Site) -> None:
        self.site = site


class CrawlRequestMsg(BaseMsg):
    """
    Request to Crawl.

    SiteActor -> CrawlActor
    """

    def __init__(self, url: str, save_dir: str, snap: bool) -> None:
        self.url = url
        self.save_dir = save_dir
        self.snap = snap


class CrawlResponseMsg(BaseMsg):
    """
    Response to a Crawl.

    CrawlActor -> SiteActor
    """

    def __init__(self, url: str, urls: Set[str]) -> None:
        self.url = url
        self.urls = urls


class CrawlSaveMsg(BaseMsg):
    """
    Save The Data of a crawl session

    CrawlActor -> SaveActor
    """

    def __init__(self, data: dict, save_dir: str) -> None:
        self.data = data
        self.save_dir = save_dir


class ScreenShotRequestMsg(BaseMsg):
    """
    Request to Take a ScreenShot
    CrawlActor -> ScreenShotActor
    """

    def __init__(self, url: str, save_dir: str) -> None:
        self.url = url
        self.save_dir = save_dir
