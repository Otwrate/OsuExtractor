from io import StringIO

import numpy as np
import pandas as pd

from OsuExtractor.DataBuilders.DataFrameBuilder import DataFrameBuilder
from OsuExtractor.DataBuilders.HitObjectsData.HitSoundType import HitSoundType
from OsuExtractor.DataBuilders.HitObjectsData.ObjectType import ObjectType
from OsuExtractor.DataBuilders.IBuilder import IBuilder
from OsuExtractor.DataBuilders.supporting_fuctions import get_type_from_bytes, get_colors_to_skip, \
    get_sound_type_from_bytes
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
        extracted = pd.DataFrame(index=raw_df.index)
        extracted[['x', 'y', 'time']] = raw_df[['x', 'y', 'time']]
        extracted['type'] = self._build_type(raw_df['type'])
        curve = extracted[extracted.type == ObjectType.Slider]

        hit_samples = pd.Series(None, index=raw_df.index)
        hit_samples[curve.index] = raw_df.iloc[curve.index]['hitSample']
        hit_samples[~hit_samples.index.isin(curve.index)] = raw_df[~raw_df.index.isin(curve.index)]['curve']
        extracted[['normalSet_hitsample', 'additionSet_hitsample', 'index_hitsample', 'volume_hitsample',
                   'filename_hitsample']] = self._build_hit_sample(hit_samples)

        extracted['is_new_combo'] = self._build_new_combo_flag(raw_df['type'])
        extracted['colors_to_skip'] = self._build_colors_to_skip(raw_df['type'])
        extracted['hitSound'] = self._build_hit_sound(raw_df['hitSound'])
        extracted['is_finish'] = self._build_is_finish(raw_df['hitSound'])

        curve_type = pd.Series(np.nan, index=raw_df.index)
        curve_points = pd.Series(np.nan, index=raw_df.index)
        parsed_curve = self._parse_curve(raw_df['curve'])
        curve_type[curve.index] = parsed_curve['type']
        curve_points[curve.index] = parsed_curve['points']

        extracted['curve_type'] = curve_type
        extracted['curve_points'] = curve_points

        extracted['edge_sound'] = self._build_edge_sound(raw_df['edgeSounds'].dropna())
        extracted['edge_set'] = self._build_edge_set(raw_df['edgeSets'].dropna())

        extracted['length'] = raw_df['length']
        extracted['slides'] = raw_df['slides']

        return extracted

    def _build_type(self, type_seres: pd.Series):
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
        return type_series.apply(get_colors_to_skip)

    def _build_hit_sound(self, hit_sound_series: pd.Series):
        return pd.Series([get_sound_type_from_bytes(x) for x in hit_sound_series], dtype=object)

    def _build_hit_sample(self, hit_sample_series: pd.Series):
        hit_samples = pd.DataFrame(hit_sample_series.apply(lambda x: pd.Series(str(x).split(':'))))
        hit_samples.columns = ['normalSet', 'additionSet', 'index', 'volume', 'filename']
        return hit_samples

    def _build_edge_sound(self, edge_sound_series: pd.Series):
        return edge_sound_series.dropna().apply(
            lambda x: np.asarray([get_sound_type_from_bytes(int(t)) for t in x.split('|')], dtype=object))

    def _build_edge_set(self, edge_set_series: pd.Series):
        split_per_edge_sound = edge_set_series.dropna().apply(lambda x: x.split('|'))
        return split_per_edge_sound.apply(lambda row: np.asarray([x.split(':') for x in row], dtype=int))

    def _build_is_finish(self, hit_sound_series: pd.Series):
        return hit_sound_series.apply(lambda x: (int(x) >> 3) % 2 == 1).astype(bool)
