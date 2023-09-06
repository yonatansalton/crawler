from abc import ABC, abstractmethod

class DataHandler(ABC):

    @abstractmethod
    def save(self, data):
        """
        Save the data.

        Args:
            data: The data to save.
        """
        pass
