from dataclasses import dataclass

from argparse import Namespace

@dataclass
class RunningConfig:
    html_file: str
    debug: bool = False
    base_path_css: str = None
    base_path_images: str = None
    base_path_javascript: str = None

    @classmethod
    def from_cli(cls, parsed: Namespace):
        return cls(**{k: v for k, v in parsed.__dict__.items() if v is not None})

__all__ = ("RunningConfig", )
