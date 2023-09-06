import threading
import json
import os
from Abstracts import DataHandler
import queue

class FileHandler(threading.Thread, DataHandler):
    '''
    Data Handler class. Inherits threadind.Thread and used to save the data coming from the crawler
    '''
    def __init__(self, logger, queue):
        super().__init__()
        self.queue = queue
        self.log = logger
        os.makedirs("./Data", exist_ok=True)
        self.counter = 0

    def save(self, data):
        '''
        This function saves the data into a file
        :param data: Dictionary coming from the crawler thread
        :return: None
        '''
        filename = data['Url'].split('//')[1].split('/')[0] + "_" + str(self.counter)
        with open(f"./Data/{filename}_t{data['Thread']}.json", "w") as f:
            json.dump(data, f)
            self.counter += 1

    def run(self):
        '''
        This is the main thread function. pops a data block from the queue and send it to the file save function.
        working until timeout is reached
        :return:
        '''
        while True:
            try:
                data = self.queue.get(timeout=10)
            except queue.Empty:
                break
            if data is None:
                break
            self.save(data)
