from typing import Type

from OsuExtractor.DataBuilders.IBuilder import IBuilder
from OsuExtractor.DataClasses.DifficultyData import DifficultyData
from OsuExtractor.DataClasses.EditorData import EditorData
from OsuExtractor.DataClasses.GeneralData import GeneralData
from OsuExtractor.DataClasses.IDataStructure import IDataStructure
from OsuExtractor.DataClasses.MetaData import MetaData


class MappableDataBuilder(IBuilder):
    def __init__(self, cls: Type[IDataStructure]) -> None:
        self.cls = cls
        self.name_mapper = {'GeneralData': 'General',
                            'EditorData': 'Editor',
                            'MetaData': 'Metadata',
                            'DifficultyData': 'Difficulty',
                            }

    def build(self, parsed_data: dict) -> IDataStructure:
        raw_data = parsed_data[self.name_mapper[self.cls.__name__]]
        casted_data = self._cast_data_types(raw_data)
        return self.cls(**casted_data)

    def _cast_data_types(self, raw_data: dict) -> dict:
        for k, v in self.cls.__annotations__.items():
            try:
                raw_data[k] = v(raw_data[k])
            except KeyError:
                raw_data[k] = None
        return raw_data
