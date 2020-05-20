from pathlib import Path

import crawler

base_dir = "dir_for_testing/"


def test_search_file1():
    """This is just a dummy test to get started."""
    files = []
    path = Path(base_dir)
    with open((path / "one.py"), "r") as f:
        files = crawler.search_file(f, str(path / "one.py"), files)
    assert len(files) == 1
