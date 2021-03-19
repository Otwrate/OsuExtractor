from typing import Type

import pandas as pd

from OsuExtractor.DataBuilders.HitObjectsDataBuilder import HitObjectsDataBuilder
from OsuExtractor.DataBuilders.MappableDataBuilder import MappableDataBuilder
from OsuExtractor.DataBuilders.DataFrameBuilder import DataFrameBuilder
from OsuExtractor.DataClasses.DifficultyData import DifficultyData
from OsuExtractor.DataClasses.EditorData import EditorData
from OsuExtractor.DataClasses.GeneralData import GeneralData
from OsuExtractor.DataClasses.IDataStructure import IDataStructure
from OsuExtractor.DataClasses.MetaData import MetaData
from OsuExtractor.DataClasses.TimingPointsData import TimingPointsData


class OsuFileReader():
    def __init__(self, mappable_classes=(GeneralData, EditorData, MetaData, DifficultyData),
                 class_names=('General', 'Editor', 'Metadata', 'Difficulty'),
                 not_mappable_classes=('Colors', 'Events', 'TimingPoints', 'HitObjects'),
                 hit_objects_columns=(
                         'x', 'y', 'time', 'type', 'hitSound', 'curve', 'slides', 'length', 'edgeSounds', 'edgeSets',
                         'hitSample'),
                 timing_points_columns=(
                         'time', 'beatLength', 'meter', 'sampleSet', 'sampleIndex', 'volume', 'uninherited',
                         'effects')):

        self.timing_points_columns = timing_points_columns
        self.hit_objects_columns = hit_objects_columns
        self.not_mappable_classes = not_mappable_classes
        self.mappable_classes = mappable_classes
        self.class_names = class_names

    def parse_to_dict(self, osu_file):
        f_new_class = False
        output = {}
        with open(osu_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip('\n')
                if line.startswith('['):
                    class_name = line.strip('[').strip(']')
                    f_new_class = True
                    parsed_container = {}

                elif f_new_class and line not in ("", " "):
                    if class_name in self.class_names:
                        parsed_container.update({line.split(':')[0]: line.split(':')[1]})

                    else:
                        if len(parsed_container) == 0:
                            parsed_container = []
                        parsed_container.append(line)

                elif f_new_class:
                    output.update({class_name: parsed_container})
                    parsed_container = {}
                    f_new_class = False
        if class_name not in output:
            output.update({class_name: parsed_container})

        return output

    def create_object(self, parsed_dict: dict):
        osu_object = {}
        for cls in self.mappable_classes:
            osu_object.update({cls.__name__: self._build_mappable_data_structure(parsed_dict, cls)})
        osu_object.update({'TimingPointsData': self._build_timing_points_data_structure(parsed_dict['TimingPoint'])})
        osu_object.update({'HitObjectsData': self._build_hit_objects_data_structure(parsed_dict['HitObjects'])})

    def _build_mappable_data_structure(self, parsed_dict: dict, cls: Type[IDataStructure]) -> IDataStructure:
        builder = MappableDataBuilder(cls)
        return builder.build(parsed_dict)

    def _build_timing_points_data_structure(self, raw_data: list) -> TimingPointsData:
        builder = DataFrameBuilder(columns=self.timing_points_columns)
        return builder.build(raw_data)

    def _build_hit_objects_data_structure(self, raw_data: list) -> TimingPointsData:
        builder = HitObjectsDataBuilder(columns=self.hit_objects_columns)
        return builder.build(raw_data)
