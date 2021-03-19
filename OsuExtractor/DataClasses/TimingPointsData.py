from dataclasses import dataclass
import pandas as pd

from OsuExtractor.DataClasses.IDataStructure import IDataStructure


@dataclass
class TimingPointsData(IDataStructure):
    df: pd.DataFrame()















