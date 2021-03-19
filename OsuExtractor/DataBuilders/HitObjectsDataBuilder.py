from io import StringIO

import numpy as np
import pandas as pd

from OsuExtractor.DataBuilders.DataFrameBuilder import DataFrameBuilder
from OsuExtractor.DataBuilders.HitObjectsData.HitSoundType import HitSoundType
from OsuExtractor.DataBuilders.HitObjectsData.ObjectType import ObjectType
from OsuExtractor.DataBuilders.IBuilder import IBuilder
from OsuExtractor.DataClasses.IDataStructure import IDataStructure
from OsuExtractor.DataClasses.TimingPointsData import TimingPointsData


class HitObjectsDataBuilder(DataFrameBuilder):
    def __init__(self, curve_types=('P', 'B', 'L', 'C'), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curve_types = curve_types

    def build(self, parsed_data: list) -> TimingPointsData:
        def to_enum(x):
            return ObjectType(x.loc['type'])

        raw_df = self._read_as_csv(parsed_data)
        raw_df.columns = self.columns
        # t = raw_df.apply(to_enum, axis=1)
        raw_df['is_new_combo'] = self._build_new_combo_flag(raw_df['type'])
        raw_df['colors_to_skip'] = self._build_colors_to_skip(raw_df['type'])
        raw_df['type'] = self._build_type(raw_df['type'])
        raw_df['hitSound'] = self._build_hit_sound(raw_df['hitSound'])
        raw_df[['normalSet_hitsample', 'additionSet_hitsample', 'index_hitsample', 'volume_hitsample',
                'filename_hitsample']] = self._build_hit_sample(raw_df['hitSample'])
        curve = raw_df[raw_df.type == ObjectType.Slider]
        raw_df[['curve_type', 'curve_points']] = self._parse_curve(curve['curve'])

        raw_df['edge_sound'] = self._build_edge_sound(curve['edgeSounds'])
        raw_df['edge_set'] = self._build_edge_set(curve['edgeSets'])
        raw_df = raw_df.drop('curve', axis=1)
        pass
        return raw_df

    def _build_type(self, type_seres: pd.Series):
        def get_type_from_bytes(x):
            if x % 2 == 1:
                return ObjectType.HitCircle
            elif (x >> 1) % 2 == 1:
                return ObjectType.Slider
            elif (x >> 3) % 2 == 1:
                return ObjectType.Spinner
            elif (x >> 7) % 2 == 1:
                return ObjectType.Hold

        return pd.Series([get_type_from_bytes(x) for x in type_seres], dtype=object)

    def _parse_curve(self, curves: pd.Series):
        def to_array(curve):
            return np.array([np.array(x.split(':')).astype(int) for x in curve[1:]])

        parsed_curves = curves.apply(lambda x: x.split('|'))
        filtered_curves = parsed_curves[parsed_curves.apply(lambda x: True if x[0] in self.curve_types else False)]
        curve_types = filtered_curves.apply(lambda x: x[0])
        curve_points = filtered_curves.apply(to_array)
        return pd.DataFrame({'type': curve_types, 'points': curve_points})

    def _build_new_combo_flag(self, type_series):
        return type_series.apply(lambda x: (x >> 2) % 2).astype(bool)

    def _build_colors_to_skip(self, type_series: pd.Series):
        def get_colors_to_skip(x):
            if (x >> 4) % 2 == 1:
                return 1
            elif (x >> 5) % 2 == 1:
                return 2
            elif (x >> 6) % 2 == 1:
                return 3
            else:
                return 0

        return type_series.apply(get_colors_to_skip)

    def _build_hit_sound(self, hit_sound_series: pd.Series):
        def get_type_from_bytes(x):
            if x % 2 == 1:
                return HitSoundType.Normal
            elif (x >> 1) % 2 == 1:
                return HitSoundType.Whistle
            elif (x >> 2) % 2 == 1:
                return HitSoundType.Finish
            elif (x >> 3) % 2 == 1:
                return HitSoundType.Clap

        return pd.Series([get_type_from_bytes(x) for x in hit_sound_series], dtype=object)

    def _build_hit_sample(self, hit_sample_series: pd.Series):
        hit_samples = pd.DataFrame(hit_sample_series.apply(lambda x: pd.Series(str(x).split(':'))))
        hit_samples.columns = ['normalSet', 'additionSet', 'index', 'volume', 'filename']
        return hit_samples

    def _build_edge_sound(self, edge_sound_series: pd.Series):
        return edge_sound_series.dropna().apply(lambda x: np.asarray(x.split('|'), dtype=int))

    def _build_edge_set(self, edge_set_series: pd.Series):
        split_per_edge_sound = edge_set_series.dropna().apply(lambda x: x.split('|'))
        return split_per_edge_sound.apply(lambda row: np.asarray([x.split(':') for x in row], dtype=int))
