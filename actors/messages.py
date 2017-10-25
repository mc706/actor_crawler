from typing import List


class BaseMsg:
    """
    Base Message
    """
    pass


class CrawlRequestMsg(BaseMsg):
    """
    Request to Crawl
    """

    def __init__(self, url: str) -> None:
        self.url = url


class CrawlResponseMsg(BaseMsg):
    """
    Response to a Crawl
    """

    def __init__(self, urls: List[str]) -> None:
        self.urls = urls


class CrawlSaveMsg(BaseMsg):
    """
    Save The Data of a crawl session
    """

    def __init__(self, data: dict) -> None:
        self.data = data


class ScreenShotRequestMsg(BaseMsg):
    """
    Request to Take a ScreenShot
    """

    def __init__(self, url: str, save_dir: str) -> None:
        self.url = url
        self.save_dir = save_dir
