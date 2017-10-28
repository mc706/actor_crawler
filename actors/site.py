import os
import pprint
from datetime import datetime
import time
from urllib.parse import urlparse

from thespian.actors import ActorTypeDispatcher, ActorExitRequest
from tqdm import tqdm

from actors.messages import CrawlRequestMsg, CrawlResponseMsg, SiteStartMsg, SiteFinishMsg
from actors.decorator import log_arguments


class SiteActor(ActorTypeDispatcher):
    """
    Actor Responsible for Controlling the Site Crawling Session
    """
    maximum_sessions = 25

    def crawl(self):
        """
        Start crawling session
        """

        for url in self.urls.copy():
            if url in self.visited_urls or url in self.in_flight_urls:
                self.urls.remove(url)
        self.progress.total = (len(self.urls) + len(self.in_flight_urls) + len(self.visited_urls))
        self.progress.update(len(self.visited_urls) - self.last_length)
        while self.urls and len(self.in_flight_urls) <= self.maximum_sessions:
            url = self.urls.pop()
            self.in_flight_urls.add(url)
            crawl_request = CrawlRequestMsg(
                url=url,
                save_dir=self.save_dir,
                snap=self.site.screen_shot,
                save_links=self.site.output_links
            )
            self.send(self.crawl_actor, crawl_request)
        if not self.urls and not self.in_flight_urls:
            log.info("Finished scraping")
            now = time.time()
            elasped = now - self.started
            message = SiteFinishMsg(
                output_file=self.save_dir + '/pages.json',
                time_elapsed=elasped
            )
            self.send(self.suite_actor, message)

    @log_arguments
    def receiveMsg_SiteStartMsg(self, message: SiteStartMsg, sender: ActorTypeDispatcher) -> None:
        """
        Site Start
        """
        site = message.site
        self.started = time.time()
        self.suite_actor = sender
        self.site = site
        self.run_name = f"crawl_{datetime.now().isoformat()}"
        self.urls: set = site.entry_points.copy()
        self.in_flight_urls = set()
        self.visited_urls = set()
        self.save_dir = os.path.join('sites', site.key, self.run_name)
        os.mkdir(self.save_dir)
        self.crawl_actor = self.createActor('actors.crawler.CrawlActor')
        self.progress = tqdm(total=(len(self.urls) + len(self.in_flight_urls) + len(self.visited_urls)))
        self.last_length = 0
        self.crawl()

    @log_arguments
    def receiveMsg_CrawlResponseMsg(self, message: CrawlResponseMsg, sender: ActorTypeDispatcher) -> None:
        """
        Crawler responds with the found url
        """
        url = message.url
        self.in_flight_urls.remove(url)
        self.last_length = len(self.visited_urls)
        self.visited_urls.add(url)
        for found_url in (message.urls - (self.in_flight_urls | self.visited_urls | self.urls)):
            if self.is_same_domain(found_url):
                self.urls.add(found_url)
            elif self.is_relative_url(found_url):
                self.urls.add(self.site.domain + found_url)
            elif self.site.check_third_party and self.is_same_domain(message.url):
                self.urls.add(found_url)
        self.crawl()

    @log_arguments
    def receiveMsg_ActorExitRequest(self, message: ActorExitRequest, sender) -> None:
        """
        On Shutdown
        """
        with open(os.path.join(self.save_dir, 'debug.dump.txt'), 'w') as dump:
            pp = pprint.PrettyPrinter(indent=4)
            dump.write(pp.pformat(self.__dict__))
        self.progress.close()
        self.send(self.crawl_actor, ActorExitRequest())

    def is_same_domain(self, url):
        parsed_uri = urlparse(url)
        domain = "{parsed_uri.scheme}://{parsed_uri.netloc}".format(parsed_uri=parsed_uri)
        return self.site.domain == domain

    def is_relative_url(self, url):
        return url and url.startswith('/') and len(url) > 1 and url[1] != '/'
