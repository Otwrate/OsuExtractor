from OsuExtractor.DataClasses.IDataStructure import IDataStructure


class EventsData(IDataStructure):
    Break_Periods: list[int]
    Background_and_Video_events: list[int, int, str, int, int]
    Storyboard_Layer_0_Background: list[int, int, str, int, int]
    Storyboard_Layer_1_Fail: list[int, int, str, int, int]
    Storyboard_Layer_2_Pass: list[int, int, str, int, int]
    Storyboard_Layer_3_Foreground: list[int, int, str, int, int]
    Storyboard_Sound_Samples: list[int, int, str, int, int]
