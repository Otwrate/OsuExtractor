from OsuExtractor.DataBuilders.IBuilder import IBuilder
from OsuExtractor.DataClasses.IDataStructure import IDataStructure


class EventsDataBuilder(IBuilder):
    def build(self, parsed_data: list) -> IDataStructure:
        for line in parsed_data:
            pass

