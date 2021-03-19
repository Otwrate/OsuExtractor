from dataclasses import dataclass

from OsuExtractor.DataClasses.IDataStructure import IDataStructure


@dataclass
class EditorData(IDataStructure):
    Bookmarks: list
    DistanceSpacing: float
    BeatDivisor: float
    GridSize: int
    TimelineZoom: float

