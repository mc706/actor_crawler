import requests
from bs4 import BeautifulSoup as BS
from thespian.actors import ActorTypeDispatcher, ActorExitRequest
from thespian.troupe import troupe

from actors.messages import CrawlRequestMsg, CrawlResponseMsg, CrawlSaveMsg, ScreenShotRequestMsg


@troupe(10)
class CrawlActor(ActorTypeDispatcher):
    """
    Actor Troupe responsible for scraping urls
    """

    def receiveMsg_CrawlRequestMsg(self, message: CrawlRequestMsg, sender: ActorTypeDispatcher) -> None:
        """
        Get a crawl request for a url
        """
        print("CrawlActor[CrawlRequestMsg]", message)
        result = {}
        urls = set()
        response = requests.get(message.url)
        response.encoding = 'utf-8'
        result['status_code'] = response.status_code
        result['timing'] = response.elapsed.total_seconds()
        # result['links_found'] = []
        soup = BS(response.text, 'html.parser')
        for link in soup.find_all('a'):
            urls.add(link.get('href'))
            # result['links_found'].append({
            #     'text': link.text,
            #     'href': link.get('href')
            # })
        result['page_title'] = soup.title.text
        # Respond Up with found urls
        response_msg = CrawlResponseMsg(url=message.url, urls=urls)
        self.send(sender, response_msg)
        # Save Results to file
        save_msg = CrawlSaveMsg(data=result, save_dir=message.save_dir)
        save_actor = self.createActor('actors.save.SaveActor')
        self.send(save_actor, save_msg)
        self.send(save_actor, ActorExitRequest)
        if message.snap:
            # Take ScreensShot
            screen_shot_msg = ScreenShotRequestMsg(url=message.url, save_dir=message.save_dir)
            screen_shot_actor = self.createActor('actors.screen_shot.ScreenShotActor')
            self.send(screen_shot_actor, screen_shot_msg)
