from io import StringIO
import pandas as pd

from OsuExtractor.DataBuilders.IBuilder import IBuilder
from OsuExtractor.DataClasses.IDataStructure import IDataStructure
from OsuExtractor.DataClasses.TimingPointsData import TimingPointsData


class DataFrameBuilder(IBuilder):
    def __init__(self, columns: tuple, *args, **kwargs):
        self.columns = columns

    def build(self, parsed_data: list) -> TimingPointsData:
        df = self._read_as_csv(parsed_data)
        df.columns = self.columns
        return df

    def _read_as_csv(self, parsed_data: list) -> TimingPointsData:
        return pd.read_csv(StringIO('\n'.join(parsed_data)), header=None)