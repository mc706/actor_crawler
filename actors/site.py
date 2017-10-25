import os
from datetime import datetime
from urllib.parse import urlparse

from thespian.actors import ActorTypeDispatcher, ActorExitRequest

from actors.messages import CrawlRequestMsg, CrawlResponseMsg, SiteStartMsg
from actors.models import Site


class SiteActor(ActorTypeDispatcher):
    """
    Actor Responsible for Controlling the Site Crawling Session
    """
    maximum_sessions = 10

    def crawl(self):
        """
        Start crawling session
        """
        print("SiteActor[crawl]", len(self.urls), len(self.in_flight_urls), len(self.visited_urls))
        while self.urls and len(self.in_flight_urls) <= self.maximum_sessions:
            url = self.urls.pop()
            self.in_flight_urls.add(url)
            crawl_request = CrawlRequestMsg(url=url, save_dir=self.save_dir, snap=self.site.screen_shot)
            self.send(self.crawl_actor, crawl_request)

    def receiveMsg_SiteStartMsg(self, message: SiteStartMsg, sender: ActorTypeDispatcher) -> None:
        """
        Site Start
        """
        print("SiteActor[SiteStartMsg]", message)
        site = message.site
        self.site = site
        self.run_name = f"crawl_{datetime.now().isoformat()}"
        self.urls: set = site.entry_points
        self.in_flight_urls = set()
        self.visited_urls = set()
        self.save_dir = os.path.join('sites', site.key, self.run_name)
        os.mkdir(self.save_dir)
        self.crawl_actor = self.createActor('actors.crawler.CrawlActor')
        self.crawl()

    def receiveMsg_CrawlResponseMsg(self, message: CrawlResponseMsg, sender: ActorTypeDispatcher) -> None:
        """
        Crawler responds with the found url
        """
        print("SiteActor[CrawlResponseMsg]", message)
        url = message.url
        self.in_flight_urls.remove(url)
        self.visited_urls.add(url)
        for found_url in (message.urls - (self.in_flight_urls | self.visited_urls)):
            if self.is_same_domain(found_url):
                self.urls.add(found_url)
            elif self.is_relative_url(found_url):
                self.urls.add(self.site.domain + found_url)
            elif self.site.check_third_party and self.is_same_domain(message.url):
                self.urls.add(found_url)
        self.crawl()
        if not self.urls and not self.in_flight_urls:
            self.send(self.crawl_actor, ActorExitRequest)

    def is_same_domain(self, url):
        parsed_uri = urlparse(url)
        domain = "{parsed_uri.scheme}://{parsed_uri.netloc}".format(parsed_uri=parsed_uri)
        return self.site.domain == domain

    def is_relative_url(self, url):
        return url.startswith('/') and url[1] != '/'
