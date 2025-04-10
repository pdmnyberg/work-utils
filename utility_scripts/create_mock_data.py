import json
import shutil
import os
import sys


class CopyMock:
    def __init__(self, type_map: dict[str, str], target_dir: str):
        self._type_map = {
            key.lower(): value
            for key, value in type_map.items()
        }
        self._target_dir = target_dir

    def get_mock_src(self, ext: str):
        return self._type_map[ext.lower()]

    def get_dst(self, basename: str):
        return f"{self._target_dir}/{basename}"

    def mock(self, filename: str):
        (_root, ext) = os.path.splitext(filename)
        basename = os.path.basename(filename)
        mock_src = self.get_mock_src(ext)
        dst = self.get_dst(basename)
        shutil.copyfile(mock_src, dst)


def main(path, mock_path, target_dir):
    assert os.path.isfile(path), f"List file does not exist '{path}'"
    assert os.path.isfile(mock_path), f"Mock file does not exist '{mock_path}'"
    assert os.path.isdir(target_dir), (
        f"Target directory does not exist '{target_dir}'"
    )

    mock_strategy = CopyMock(
        type_map={
            ".png": mock_path
        },
        target_dir=target_dir
    )
    with open(path, "r") as file:
        data = json.load(file)
        for filename in data:
            mock_strategy.mock(filename)


if __name__ == "__main__":
    main(*sys.argv[1:])
