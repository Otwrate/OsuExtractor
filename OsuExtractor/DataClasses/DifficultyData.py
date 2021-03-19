from dataclasses import dataclass

from OsuExtractor.DataClasses.IDataStructure import IDataStructure


@dataclass
class DifficultyData(IDataStructure):
    HPDrainRate: float
    CircleSize: float
    OverallDifficulty: float
    ApproachRate: float
    SliderMultiplier: float
    SliderTickRate: float
























