from dataclasses import dataclass

from OsuExtractor.DataClasses.IDataStructure import IDataStructure


@dataclass
class GeneralData(IDataStructure):
    AudioFilename: str
    AudioLeadIn: int
    AudioHash: str
    PreviewTime: int
    Countdown: int
    SampleSet: str
    StackLeniency: float
    Mode: int
    LetterboxInBreaks: bool
    StoryFireInFront: bool
    UseSkinSprites: bool
    AlwaysShowPlayfield: bool
    OverlayPosition: str
    SkinPreference: str
    EpilepsyWarning: bool
    CountdownOffset: int
    SpecialStyle: bool
    WidescreenStoryboard: bool
    SamplesMatchPlaybackRate: bool






















