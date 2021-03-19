import glob
from pathlib import Path

from OsuExtractor.parse_osu_file import OsuFileReader

if __name__ == '__main__':
    data_path = r"C:\Users\jklnnjhkk\PycharmProjects\pythonProject\test_data"

    reader = OsuFileReader()
    for path in Path(data_path).rglob('*.osu'):
        raw_dict = reader.parse_to_dict(path)
        reader.create_object(raw_dict)

