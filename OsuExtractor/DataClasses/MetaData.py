from dataclasses import dataclass

from OsuExtractor.DataClasses.IDataStructure import IDataStructure


@dataclass
class MetaData(IDataStructure):
    Title: str
    TitleUnicode: str
    Artist: str
    ArtistUnicode: str
    Creator: str
    Version: str
    Source: str
    Tags: str
    BeatmapID: int
    BeatmapSetID: int






















