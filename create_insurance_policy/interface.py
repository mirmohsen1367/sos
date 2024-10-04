from abc import ABC, abstractmethod


class AbstractParseData(ABC):
    @abstractmethod
    def parse_date(self, data, list_of_key, maping_key):
        pass

    @abstractmethod
    def create_data(self, data):
        """give data and parse with method pars_date and return correct format"""
        pass
