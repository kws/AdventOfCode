from pathlib import Path

import usersettings

_aoc_event = "2015"


settings = usersettings.Settings(f"kws.aoc-{_aoc_event}")
settings.add_setting("username", str)
settings.load_settings()


class Config:
    _PROJECT_DIR = Path(__file__).parent.parent
    INPUTS_DIR = _PROJECT_DIR / "inputs"
    SAMPLE_DIR = INPUTS_DIR / "samples"
    TESTS_DIR = _PROJECT_DIR / "tests"
    AOC_EVENT = _aoc_event

    @property
    def USER_DIR(self):
        return self.INPUTS_DIR / settings.username

    @property
    def PACKAGE_NAME(self):
        return f"aoc_{_aoc_event}_kws"


config = Config()
