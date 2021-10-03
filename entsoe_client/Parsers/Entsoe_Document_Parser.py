from abc import ABC, abstractmethod


class Entsoe_Document_Parser(ABC):
    def __init__(self):
        self.objectified_input_xml = None

    def set_objectified_input_xml(self, objectified_input_xml):
        self.objectified_input_xml = objectified_input_xml

    @classmethod
    @abstractmethod
    def parse(cls):
        pass
