from OsuExtractor.DataBuilders.HitObjectsData.HitSoundType import HitSoundType
from OsuExtractor.DataBuilders.HitObjectsData.ObjectType import ObjectType


def get_sound_type_from_bytes(x):
    if x % 2 == 1:
        return HitSoundType.Normal
    elif (x >> 1) % 2 == 1:
        return HitSoundType.Whistle
    elif (x >> 2) % 2 == 1:
        return HitSoundType.Clap
    else:
        return HitSoundType.Normal

def get_colors_to_skip(x):
    if (x >> 4) % 2 == 1:
        return 1
    elif (x >> 5) % 2 == 1:
        return 2
    elif (x >> 6) % 2 == 1:
        return 3
    else:
        return 0

def get_type_from_bytes(x):
    if x % 2 == 1:
        return ObjectType.HitCircle
    elif (x >> 1) % 2 == 1:
        return ObjectType.Slider
    elif (x >> 3) % 2 == 1:
        return ObjectType.Spinner
    elif (x >> 7) % 2 == 1:
        return ObjectType.Hold