import threading
import queue
import requests
from bs4 import BeautifulSoup, element
from Abstracts import Crawler

class WebCrawler(threading.Thread, Crawler):
    '''
    Crawler class. inherit threading.Thread
    '''
    def __init__(self, logger, url: str, dataQueue: queue.Queue(), concurrency: int):
        '''
        Crawler ctor
        :param logger: logger to log all events
        :param url: Main url to crawl
        :param dataQueue: The queue to put data parsed from the links
        :param concurrency: Number of threads that will be initilized to run the crawl function
        '''
        super().__init__()
        self.queue = dataQueue
        self.linkQ = queue.Queue()
        self.url = url
        self.concurrency = concurrency
        self.log = logger


    def crawl(self, tid: str):
        '''
        This is the main crawl function that runs until the linkQ queue does not return anything for 5 seconds,
        meanind it's empty. until then the while loop keeps working and pop a link from the queue.
        each link is sent to the get_document function to extract the data from it
        :param tid: string. Thread number used later on when saving the data into a file
        :return: None
        '''

        while True:
            try:
                link = self.linkQ.get(timeout=5)
            except queue.Empty:
                self.queue.put(None)
                break

            self.get_document(link, tid)

    def get_document(self, link: element.Tag, tid: str):
        '''
        This is the get_document function. it get a BS tag,
        It is then extracts the title, author, publish date and content from it and adds thread id.
        it puts the data into the data queue that is being handler by the DataHandler Thread.
        :param link: string, the url needed to extract data from
        :param tid: thread id
        :return:
        '''
        try:
            a = link.find_all('a')
            title = a[1].text
            author = a[2].text

            index = link.find("div", class_="wpf-thread-author-name").text.rfind(',') + 1
            date = link.find("div", class_="wpf-thread-author-name").text[index:].strip()
            url = a[1].get("href")
            text = ""

            try:
                response = requests.get(url, headers={"User-Agent": "XY"})
                if response.status_code == 200:
                    content = response.content
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.find("div", class_="wpforo-post-content").text

            except Exception as e:
                self.log.warning("Failed to fetch content from " + url)

            data = {
                    "Title": title,
                    "Author": author,
                    "Published": date,
                    "Url": url,
                    "Content": text,
                    "Thread": tid
                 }
            self.queue.put(data)
            self.log.info("Got document from " + url)
        except Exception as e:
            self.log.error(str(e))

    def find_documents(self, url: str):
        '''
        This function gets a url and scans it for links using BS.
        :param url:
        :return:
        '''
        try:
            response = requests.get(url, headers={"User-Agent": "XY"})

            if response.status_code == 200:
                content = response.content
                soup = BeautifulSoup(content, "html.parser")
                links = soup.find_all("div", class_="wpf-thread")
                for link in links:
                    self.linkQ.put(link)
            else:
                self.log.error("Got bad response from server " + str(response.status_code))
        except Exception as e:
            self.log.error(str(e))

    def run(self):
        '''
        Main thread function. this function first looks for links in the main url, then it starts N crawlers to handle the links
        according to the desired concurrency
        :return: None
        '''
        self.find_documents(self.url)
        threads = []
        for i in range(self.concurrency):
            thread = threading.Thread(target=self.crawl, args=(i,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.queue.put(None)
