from abc import ABC, abstractmethod

class Crawler(ABC):

    @abstractmethod
    def crawl(self):
        """
        Start Crawling

        """
        pass
