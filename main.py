import typer
import queue
import logging
from Crawlers import WebCrawler
from DataHandlers import FileHandler

def main(url, concurrency):

    q = queue.Queue()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a console handler and add it to the logger
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    # Format the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Create the threads
    crawler = WebCrawler(logger, url, q, int(concurrency))
    fileHandler = FileHandler(logger, q)

    # Start the threads
    crawler.start()
    fileHandler.start()

    # Wait for the threads to finish
    crawler.join()
    fileHandler.join()


typer.run(main)